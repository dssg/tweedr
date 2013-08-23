# Extraction Tool

This tool can be used to create labeled data from tweets. 

## Setup Database for tweet output

* [`doc/`](doc) contains various presentations, along with accompanying slides and poster.
    + [`doc/report/`](doc/report) contains a more technical and extensive write-up of this project. _In progress._
* `ext/` is created by a complete install; external data sources and libraries are downloaded to this folder.
* [`static/`](static) contains static (non-Javascript) files used by the web app.
* [`templates/`](templates) contain templates (both server-side and client-side) used by the web app.
* [`tests/`](tests) contain unittest-like tests. Use `python setup.py test` to run these.
* [`tools/`](tools) holds tools to aid development (currently, only a test-running git-hook).
* [`tweedr/`](tweedr) contains the main Python app and functions as a Python package (e.g., `import tweedr`).


## Contact

Want to get in touch? Found a bug? Open up a [new issue](https://github.com/dssg/tweedr/issues/new) or email us at [dssg-qcri@googlegroups.com](mailto:dssg-qcri@googlegroups.com).


## License

Copyright © 2013 The University of Chicago. [MIT Licensed](LICENSE).
