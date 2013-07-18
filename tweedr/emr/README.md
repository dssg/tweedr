## Examples for the wordcounter

Run the counter locally (using some data that's on the qcri machine):

    python gnip_wc.py /home/chbrown/data/gnip/christchurch/2011-02-28*.json.gz

That particular example glob is about 15MB compressed, 107MB uncompressed, 59704 lines (= tweets).

It runs in about 2m 30s locally, on the qcri AWS machine.

Or run on EMR, using the same glob, but from S3.

    python gnip_wc.py -r emr s3://qcri/gnip/christchurch/2011-02-28*.json.gz --output-dir "s3://qcri/tmp-`date +%s`"

This took about 21m, without specifying any numbers. From the docs:

> By default, **mrjob** runs a single `m1.small`, which is a cheap but not very powerful instance type.

Trying a few more instances at once:

    !! --num-ec2-instances 2

Hmm. Still took 21 minutes.

    !! --num-ec2-instances 4

Better! Took 13m. I think most of this is overhead in starting the cluster.

    !! --num-ec2-instances 8

Overkill, apparently. Took 13m again.

Could also try some different types:

    --ec2_instance_type c1.medium

(Umm... later.)

How about all of christchurch?

    python gnip_wc.py -r emr --num-ec2-instances 8 s3://qcri/gnip/christchurch/*.json.gz

That's 757,382 tweets, 270MB compressed = 1.7GB uncompressed, simple word count took 1h 12m (apparently it only took 53m, as billed by AWS, so $(.12+.03) * 8 = $1.20), produced 12 output files for a total of ~12MB (uncompressed).

## Running a full geolocation task:

    cd ~/src/qcri/emr
    output_dir="s3://qcri/tmp-`date +%s`"
    echo Using $output_dir as our output directory
    time python gnip_geo.py --containers gnip_containers.geojson \
      s3://qcri/gnip/*/*.json.gz --output-dir $output_dir -r emr --num-ec2-instances 5

## Examples

Some of the fields from a geolocated tweet might look like this. Note that the coordinates are `[lat,lng]`.

    {
      ...
      "gnip": {
        "matching_rules": [
          {
            "value": "has:geo",
            "tag": "westtx:geo"
          }
        ],
        ...
      },
      ...
      "geo": {
        "type": "Point",
        "coordinates": [
          31.4119232,
          -86.1200234
        ]
      },
      ...
    }

And here's some GeoJSON, for reference (because Polygons are weird, allowing inner rings):

    { "type": "Polygon",
      "coordinates": [
        [
          [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
        ]
      ]
    }

But Points are easier:

    { "type": "Point", "coordinates": [100.0, 0.0] }
