from tweedr.ark.java import TwitterNLP

import logging
logger = logging.getLogger(__name__)

logger.debug('The TwitterNLP POS tagger is being loaded as a module singleton')

# simply by importing this module, the TwitterNLP tagger will be started up and
# made available to other scripts.
tagger = TwitterNLP()
