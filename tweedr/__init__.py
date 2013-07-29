import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# just resolve this file in the context of the current working directory
# and find the parent of its directory
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
