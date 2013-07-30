import os
import logging
import random

import bottle
from bottle import request, redirect, static_file, mako_view as view

import tweedr
from tweedr.lib.text import token_re
from tweedr.ml import crf
from tweedr.ml.features import crf_feature_functions, featurize
from tweedr.models import DBSession, TokenizedLabel

logger = logging.getLogger(__name__)

# tell bottle where to look for templates
bottle.TEMPLATE_PATH.append(os.path.join(tweedr.root, 'templates'))

# this is the primary export
app = bottle.Bottle()

# globals are messy, but we don't to retrain a tagger for every request
GLOBALS = dict(tagger=None)


def initialize():
    query = DBSession.query(TokenizedLabel).limit(1000)
    logger.debug('initializing %s', __name__)
    tmp_filepath = '/tmp/tweedr.ui.crf.model'
    tagger = crf.Tagger.from_path_or_data(query, crf_feature_functions, model_filepath=tmp_filepath)
    GLOBALS['tagger'] = tagger

initialize()


@app.get('/')
def root():
    redirect('/crf')


@app.get('/crf')
@view('crf.mako')
def index():
    return dict()


@app.get('/tokenized_labels/sample')
def tokenized_labels_sample():
    total = DBSession.query(TokenizedLabel).count()
    index = random.randrange(total)
    logger.debug('/random_text: choosing #%d out of %d', index, total)
    tokenized_label = DBSession.query(TokenizedLabel).offset(index).limit(1).first()
    return tokenized_label.__json__()


@app.post('/tagger/tag')
def tagger_tag():
    # For bottle >= 0.10, request.forms.xyz attributes return unicode strings
    # and an empty string if decoding fails.
    text = request.forms.text
    tokens = token_re.findall(text.encode('utf8'))

    tokens_features = featurize(tokens, crf_feature_functions)
    tagger = GLOBALS['tagger']
    labels = list(tagger.tag_raw(tokens_features))

    return {
        'sequences': [
            {'name': 'tokens', 'values': tokens},
            {'name': 'features', 'values': [' '.join(token_features) for token_features in tokens_features]},
            {'name': 'labels', 'values': labels},
        ]
    }


@app.route('/tagger/retrain')
def tagger_retrain():
    query = DBSession.query(TokenizedLabel).limit(10000)
    tagger = crf.Tagger.from_path_or_data(query, crf_feature_functions)
    GLOBALS['tagger'] = tagger
    return dict(success=True)


@app.route('/static/<filepath:path>')
def serve_static_file(filepath):
    return static_file(filepath, os.path.join(tweedr.root, 'static'))


@app.route('/templates/<filepath:path>')
def serve_templates_file(filepath):
    return static_file(filepath, os.path.join(tweedr.root, 'templates'))
