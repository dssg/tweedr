import os
import time
import tempfile

import bottle
from bottle import request
from bottle import mako_view as view  # , mako_template as template

import tweedr
from tweedr.lib import flatten
from tweedr.lib.text import token_re
from tweedr.ml import crf
from tweedr.ml.features import all_feature_functions
from tweedr.models import DBSession, TokenizedLabel


# tell bottle where to look for templates
template_path = os.path.join(os.path.dirname(tweedr.__file__), '..', 'templates')
bottle.TEMPLATE_PATH.insert(0, template_path)

app = bottle.Bottle()


# globals are messy, but we don't to retrain a tagger for every request
GLOBALS = dict(tagger=None)


def train_tagger(max_training=1000):
    query = DBSession.query(TokenizedLabel).limit(max_training)
    print 'Training tagger on %d instances' % query.count()
    trainer = crf.Trainer()
    for tokenized_label in query:
        tokens = tokenized_label.tokens
        labels = tokenized_label.labels
        data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))
        trainer.append_raw(data, labels)

    model_path = tempfile.NamedTemporaryFile(delete=False).name
    trainer.save(model_path)
    print 'Trainer saved to ' + model_path
    return crf.Tagger(model_path)


@app.get('/')
@view('crf.mako')
def index():
    return dict()


@app.post('/annotate')
def annotate():
    started = time.time()
    text = request.forms.get('text')
    tokens = token_re.findall(text.encode('utf8'))
    data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))
    tagger = GLOBALS['tagger']
    labels = list(tagger.tag_raw(data))

    duration = time.time() - started
    return dict(tokens=tokens, labels=labels, duration=duration)

if __name__ == '__main__':
    GLOBALS['tagger'] = train_tagger()
    app.run(reloader=False)
