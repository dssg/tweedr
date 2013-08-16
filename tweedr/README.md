## Tweedr Python package

* [`api/`](api) contains the main "pipeline" command line tool
* [`emr/`](emr) contains scripts for running jobs on Elastic Map Reduce
* [`lib/`](lib) holds miscellaneous helpers or basic text manipulation tools.
* [`ml/`](ml) contains all the machine learning and natural language processing tools.
* [`models/`](models) holds the database schema and relationship definitions.
* [`ui/`](ui) contains the web application.
* [`__init__.py`](__init__.py) contains extensive log configuration.

## Use

After installing, `tweedr` can be used as a Python package:

    import tweedr
    print tweedr.__version__
