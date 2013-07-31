import os
import logging

# just resolve this file in the context of the current working directory
# and find the parent of its directory
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add SILLY loglevel (above notset=0, below debug=10)
SILLY = 5
logging.addLevelName(SILLY, 'SILLY')


class TweedrLogger(logging.Logger):
    def silly(self, msg, *args, **kwargs):
        if self.isEnabledFor(SILLY):
            self._log(SILLY, msg, args, **kwargs)

    def __repr__(self):
        return '<%s name=%s level=%d (effective=%d) disabled=%d>' % (self.__class__.__name__,
            self.name, self.level, self.getEffectiveLevel(), self.disabled)

default_level = logging.DEBUG

logging.basicConfig(level=default_level)
logging.setLoggerClass(TweedrLogger)

logger = logging.getLogger(__name__)
