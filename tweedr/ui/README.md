## UI configuration and installation

Make sure these environment variables are available to the python server process:

    export MYSQL_HOST="qcri.abcdefghijkl.us-west-2.rds.amazonaws.com"
    export MYSQL_USER="yourusername"
    export MYSQL_PASS="andthepassword"
    export MYSQL_DATABASE="finallythedatabasename"

Ensure that `tweedr-ui` is linked into your PATH:

    python setup.py develop

And run it:

    tweedr-ui

Alternatively, you can run it from the package's base directory:

    python tweedr/ui/__init__.py

## Browsing

As you can see from the output of that call, Bottle serves the application on port 8080 by default.

* [localhost:8080](http://127.0.0.1:8080/)

This should redirect you to `/crf` — take a look at your developer console in the browser to see the endpoints it's hitting to find new tweets and tag them.
