from bottle import run
from tweedr.ui.middleware import add_duration_header


def main():
    '''
    This is called by the console_scripts entry_point:
        "tweedr-ui = tweedr.ui:main"

    The reloader is slow and only handles python module changes.
    I recommend using 3rd party restarter, say, node_restarter:
        node_restarter **/*.py **/*.css **/*.mako 'python tweedr/ui/__init__.py'
    '''
    # this import also triggers training the CRF tagger global in ui/crf.py
    from tweedr.ui.crf import app
    app = add_duration_header(app)
    run(app, reloader=False)

if __name__ == '__main__':
    main()
