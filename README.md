# Tweedr: Twitter for Disaster Response

<a href="http://www.qcri.com/"><img src="http://dssg.io/img/partners/qcri.png" width="400" align="right"></a>

Tweedr makes information from social media more accessible to providers of disaster relief. There are two aspects to the application:

1. An **API** / **pipeline** for applying _machine learning techniques_ and _natural language processing tools_ to analyze social media produced in response to a disaster.
2. A **user interface** for manipulating, filtering, and aggregating this enhanced social media data.

Tweedr is a [Data Science for Social Good](http://dssg.io/) project, through a partnership with the [Qatar Computational Research Institute](http://qcri.qa/).

## Problem, solution, data

![web app screenshot](https://raw.github.com/dssg/dssg.github.io/master/img/posts/tweedr-screenshot.png)

* For an extensive discussion of the problem and proposed solution, [visit our wiki](https://github.com/dssg/tweedr/wiki).
* Get start using the tweedr api, [check out our tutorial website](http://tokens.qcri.dssg.io/tweedrtutorial/).


## Project layout

* [`doc/`](doc) contains various presentations, along with accompanying slides and poster.
    + [`doc/report/`](doc/report) contains a more technical and extensive write-up of this project. _In progress._
* `ext/` is created by a complete install; external data sources and libraries are downloaded to this folder.
* [`static/`](static) contains static (non-Javascript) files used by the web app.
* [`templates/`](templates) contain templates (both server-side and client-side) used by the web app.
* [`tests/`](tests) contain unittest-like tests. Use `python setup.py test` to run these.
* [`tools/`](tools) holds tools to aid development (currently, only a test-running git-hook).
* [`tweedr/`](tweedr) contains the main Python app and functions as a Python package (e.g., `import tweedr`).


## Installation guide

    git clone https://github.com/dssg/tweedr.git
    cd tweedr
    python setup.py develop download_ext

If you want to jump straight to development, see the [Contributing](https://github.com/dssg/tweedr/wiki/Contributing) wiki page.

### Dependencies

Tweedr uses a number of external libraries and resources. This is the dependency tree:

* [Tweedr](https://github.com/dssg/tweedr): Primarily python, on github
    - [crfsuite](http://www.chokkan.org/software/crfsuite/): C/C++, from source
        + [libLBFGS](http://www.chokkan.org/software/liblbfgs/): C/C++, from source
    - [scikit-learn](http://scikit-learn.org/stable/): Python, from PyPI
        + [numpy](http://www.numpy.org/): Python, with C/C++ (blas/lapack), Fortran links, from PyPI or package manager
        + [scipy](http://www.scipy.org/): Python, with C/C++, from PyPI or package manager
    - [TweetNLP](http://www.ark.cs.cmu.edu/TweetNLP/): Java, from jar
    - [PyPer] (https://pypi.python.org/pypi/PypeR/1.1.0): Python, with R, from PyPI

`crfsuite` and `liblbfgs` are the only components that can't be installed directly with Python via `setuptools`. Though if you have trouble installing some of the packages above, you might have better luck looking for those packages in your operating system's pacakge manager or as binaries on the projects' websites.

### Installation steps

*1. Installing libLBFGS*

The source code can be downloaded from the [maintainer's webpage](http://www.chokkan.org/software/liblbfgs/), though this [Github fork](https://github.com/chbrown/liblbfgs) (and below) attempts to simplify the install process.

    git clone https://github.com/chbrown/liblbfgs.git
    cd liblbfgs
    ./configure
    make
    sudo make install

*2. Installing CRFsuite*

Like libLBFGS, a tarball can be downloaded from the [original website](http://www.chokkan.org/software/crfsuite/), though the accompanying [fork on Github](https://github.com/chbrown/crfsuite) attempts to document the installation process and make compilation more automatic on both Linux and Mac OS X.

    git clone https://github.com/chbrown/crfsuite.git
    cd crfsuite
    ./configure
    make
    sudo make install

That installs the library, but not the Python wrapper, which takes a few more steps:

    cd swig/python
    python setup.py build_ext
    sudo python setup.py install_lib

To test whether it installed correctly, you can run the following at your terminal, which should print out the current CRFsuite version:

    python -c 'import crfsuite; print crfsuite.version()'
    > 0.12.2

The [github repository](https://github.com/chbrown/crfsuite) documents a few more options that might come in handy if the process above does not work for your operating system.


*3. Configuring environment variables*

Tweedr also connects to a number of remote resources when running live; see [[Environment]] for instructions on setting those up.


*4. Installing Tweedr*

After installing `crfsuite` and `liblbfgs`, everything else should be installable via setuptools / distutils:

    git clone https://github.com/dssg/tweedr.git
    cd tweedr
    python setup.py install

And then to download external data requirements:

    python setup.py download_ext

The `download_ext` command will download external data, which currently includes the following packages / sources:

* [TweetNLP 0.3.2 tarball](http://ark-tweet-nlp.googlecode.com/files/ark-tweet-nlp-0.3.2.tgz) (Github repository: [ark-tweet-nlp](https://github.com/brendano/ark-tweet-nlp))

You may get an error, "IOError: cmu.arktweetnlp.RunTagger error", if you try to use some parts of Tweedr before installing this component.


*5. Instantiating the database*

While we are not currently able to release our data, you can easily recreate the structure of our database by running the following command:

    tweedr-database create

This simply uses SQLAlchemy to un-reflect the database, by running `metadata.create_all()`.


### Running Tweedr

At this point, you should have tools like `tweedr-ui` and `tweedr-pipeline` on your `PATH`, and you can run each of those with the `--help` flag to view the usage messages.

See [the API section](https://github.com/dssg/tweedr/wiki#tweedr-api-how-it-works) of the wiki for a description of some of the fields that `tweedr-pipeline` adds.


### Troubleshooting

If your installation is still missing packages, see the [manually installing](https://github.com/dssg/tweedr/wiki/Manually-installing) page of the wiki.


## Team
![Team](https://raw.github.com/dssg/dssg.github.io/761993c24ea2991170ef64048115cb805f5f13fb/img/people/teams/tweedr.png)


## Contributing to the project

Want to get in touch? Found a bug? Open up a [new issue](https://github.com/dssg/tweedr/issues/new) or email us at [dssg-qcri@googlegroups.com](mailto:dssg-qcri@googlegroups.com).


## License

Copyright © 2013 The University of Chicago. [MIT Licensed](LICENSE).
