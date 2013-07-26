# this import also triggers training the CRF tagger global in ui/crf.py
from tweedr.ui.crf import app


def main():
    app.run(reloader=False)

if __name__ == '__main__':
    main()
