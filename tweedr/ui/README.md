## Configuration

Make sure your environment variables are available to the process that will be serving the app.

See the wiki [Environment](https://github.com/dssg/tweedr/wiki/Environment) page, particular the `MYSQL_*` variables.


## Running

The `tweedr-ui` CLI gets installed when you install tweedr. Simply run it:

    tweedr-ui


## Browsing

As you can see from the output of that call, Bottle serves the application on port 8080 by default.

* http://127.0.0.1:8080/

This should redirect you to `/crf` — take a look at your developer console in the browser to see the endpoints it's hitting to load new tweets and tag them.
