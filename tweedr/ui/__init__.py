# this import also triggers training the CRF tagger global in ui/crf.py
from bottle import run
from tweedr.ui.crf import app


def main():
    '''This is called by the console_scripts entry_point,
    "tweedr-ui = tweedr.ui:main"
    '''
    run(app, reloader=True)

if __name__ == '__main__':
    main()
