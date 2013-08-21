from bottle import run
from tweedr.ui import middleware, crf


def main():
    '''This is called by the package's console_scripts entry point "tweedr-ui"

    The reloader is slow and only handles python module changes.
    I recommend using 3rd party restarter, say, node_restarter:
        node_restarter **/*.py **/*.css **/*.mako 'python tweedr/cli/ui.py'
    '''
    app = middleware.add_duration_header(crf.app)
    run(app)

if __name__ == '__main__':
    main()
