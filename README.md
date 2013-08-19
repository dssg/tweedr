# Tweedr is Twitter for Disaster Response

Tweedr makes information from social media more accessible to providers of disaster relief. There are two aspects to the application:

1. An **API** / **pipeline** for applying _machine learning techniques_ and _natural language processing tools_ to analyze social media produced in response to a disaster.
2. A **user interface** for manipulating, filtering, and aggregating this enhanced social media data.

Tweedr is a [Data Science for Social Good](http://dssg.io/) project, through a partnership with the [Qatar Computational Research Institute](http://qcri.qa/).

See the [Project Overview](https://github.com/dssg/tweedr/wiki) for a more extensive discussion of the problem and proposed solution or check out our [tutorial website](http://tokens.qcri.dssg.io/tweedrtutorial/). 


## Project layout

* [`doc/`](doc) contains various presentations, along with accompanying slides and poster.
    + [`doc/report/`](doc/report) contains a more technical and extensive write-up of this project. _In progress._
* `ext/` is created by a complete install; external data sources and libraries are downloaded to this folder.
* [`static/`](static) contains static (non-Javascript) files used by the web app.
* [`templates/`](templates) contain templates (both server-side and client-side) used by the web app.
* [`tests/`](tests) contain unittest-like tests. Use `python setup.py test` to run these.
* [`tools/`](tools) holds tools to aid development (currently, only a test-running git-hook).
* [`tweedr/`](tweedr) contains the main Python app and functions as a Python package (e.g., `import tweedr`).


## Quickstart

    git clone https://github.com/dssg/tweedr.git
    cd tweedr
    python setup.py develop install_data

See [Deploy](https://github.com/dssg/tweedr/wiki/Deploy) on the [wiki](https://github.com/dssg/tweedr/wiki) for more help getting an instance of Tweedr up and running.

If you want to jump straight to development, see the [Contributing](https://github.com/dssg/tweedr/wiki/Contributing) wiki page.


## License

Copyright © 2013 The University of Chicago. [MIT Licensed](LICENSE).
