from sqlalchemy import orm
from tweedr.lib.text import token_re
from tweedr.models.metadata import engine

sessionmaker = orm.sessionmaker(bind=engine)
DBSession = sessionmaker()

# we write enhanced ORM classes directly on top of the schema originals,
# so that enhancements are optional and transparent
from tweedr.models import schema
from schema import *


class TokenizedLabel(schema.TokenizedLabel):
    @property
    def tokens(self):
        return token_re.findall(unicode(self.tweet).encode('utf8'))

    @property
    def labels(self):
        labels = []
        label_start, label_end = self.token_start, self.token_end
        for match in token_re.finditer(self.tweet):
            token_start, token_end = match.span()
            # token = match.group(0)
            # we want to determine if this particular token in the original tweet overlaps
            #   with any portion of the selected label (label_span)
            if label_start <= token_start <= label_end or label_start <= token_end <= label_end:
                labels.append(self.token_type)
            else:
                # should I let the user set the NA label?
                labels.append(None)
        return [unicode(label).encode('utf8') for label in labels]
