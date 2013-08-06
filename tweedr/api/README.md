## API


### Instructions for `pipeline.py`

Let's say your tweets are gzipped json files in `~/corpora/qcri/gnip_tweets/samoa/`:

    cat ~/corpora/qcri/gnip_tweets/samoa/*.json.gz | gunzip | tweedr-pipeline

* `tweedr-pipeline` is simply an alias for `tweedr.api.pipeline.main()`


### More examples

Ignore the hapaxlegomena:

    ... | tweedr-pipeline | json -C count text | grep -v $'1\t'
