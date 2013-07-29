# this import also triggers training the CRF tagger global in ui/crf.py
from bottle import run
from tweedr.ui.crf import app


def main():
    '''
    This is called by the console_scripts entry_point:
        "tweedr-ui = tweedr.ui:main"

    The reloader is slow and only handles python module changes.
    I recommend using 3rd party restarter, say, node_restarter:
        node_restarter **/*.py **/*.css **/*.mako 'python tweedr/ui/__init__.py'
    '''
    run(app, reloader=False)

if __name__ == '__main__':
    main()
