import os
import sys
import logging
from colorama import Fore, Back, Style

# just resolve this file in the context of the current working directory
# and find the parent of its directory
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add SILLY loglevel (above notset=0, below debug=10)
SILLY = 5
logging.addLevelName(SILLY, 'SILLY')


class ColorFormatter(logging.Formatter):
    # colors: https://pypi.python.org/pypi/colorama
    thresholds = [
        (logging.CRITICAL, (Back.RED, Back.RESET)),
        (logging.ERROR, (Fore.RED, Fore.RESET)),
        (logging.WARNING, (Back.YELLOW, Back.RESET)),
        (logging.INFO, (Fore.CYAN, Fore.RESET)),
        (logging.DEBUG, (Fore.GREEN, Fore.RESET)),
        (SILLY, (Style.DIM, Style.NORMAL)),
        (logging.NOTSET, ('', '')),
    ]

    def format(self, record):
        result = super(ColorFormatter, self).format(record)

        for threshold, (prefix, postfix) in self.thresholds:
            if record.levelno >= threshold:
                break
        return prefix + result + postfix


class TweedrLogger(logging.Logger):
    # def __init__(self, name, **kw):
    #     super(TweedrLogger, self).__init__(name, **kw)

    def silly(self, msg, *args, **kwargs):
        if self.isEnabledFor(SILLY):
            self._log(SILLY, msg, args, **kwargs)

    def notset(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.NOTSET):
            self._log(logging.NOTSET, msg, args, **kwargs)

    def __repr__(self):
        return '<%s name=%s level=%d (effective=%d) parent=%s disabled=%d>' % (self.__class__.__name__,
            self.name, self.level, self.getEffectiveLevel(), self.parent, self.disabled)


# the following 5 lines replace logging.basicConfig(level=default_level)
#   very similar effect, but with a color formatter.
handler = logging.StreamHandler(sys.stderr)
color_formatter = ColorFormatter(fmt='%(levelname)s:%(name)s:%(message)s')
handler.setFormatter(color_formatter)
logging.root.addHandler(handler)
logging.root.setLevel(logging.DEBUG)

logging.setLoggerClass(TweedrLogger)

logger = logging.getLogger(__name__)
