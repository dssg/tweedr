import os
import time

import bottle
from bottle import request
from bottle import mako_view as view  # , mako_template as template

import tweedr
from tweedr.lib.text import token_re
from tweedr.ml import crf
from tweedr.ml.features import all_feature_functions, featurize
from tweedr.models import DBSession, TokenizedLabel


# tell bottle where to look for templates
template_path = os.path.join(os.path.dirname(tweedr.__file__), '..', 'templates')
bottle.TEMPLATE_PATH.insert(0, template_path)

# this is the primary export
app = bottle.Bottle()

# globals are messy, but we don't to retrain a tagger for every request
GLOBALS = dict(tagger=None)


def initialize():
    query = DBSession.query(TokenizedLabel).limit(1000)
    print 'initializing', __name__
    tmp_filepath = '/tmp/tweedr.ui.crf.model'
    tagger = crf.Tagger.from_path_or_data(query, all_feature_functions, model_filepath=tmp_filepath)
    GLOBALS['tagger'] = tagger


@app.get('/')
@view('crf.mako')
def index():
    return dict()


@app.post('/annotate')
def annotate():
    started = time.time()
    text = request.forms.get('text')
    tokens = token_re.findall(text.encode('utf8'))

    tokens_features = featurize(tokens, all_feature_functions)
    tagger = GLOBALS['tagger']
    labels = list(tagger.tag_raw(tokens_features))

    duration = time.time() - started
    return dict(tokens=tokens, labels=labels, duration=duration)


@app.get('/retrain')
def retrain():
    query = DBSession.query(TokenizedLabel).limit(10000)
    tagger = crf.Tagger.from_path_or_data(query, all_feature_functions)
    GLOBALS['tagger'] = tagger
    return dict(success=True)


initialize()
