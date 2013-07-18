from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import json


def bbox_contains(bbox, longitude, latitude):
    sw_lon, sw_lat, ne_lon, ne_lat = bbox
    return (sw_lon <= longitude <= ne_lon) and (sw_lat <= latitude <= ne_lat)


class GeoExtract(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def configure_options(self):
        super(GeoExtract, self).configure_options()
        # add_file_option: http://mrjob.readthedocs.org/en/latest/guides/writing-mrjobs.html
        self.add_file_option('--containers', help='.geojson feature collection to filter for')

    def mapper_init(self):
        with open(self.options.containers) as fp:
            self.feature_collection = json.load(fp)

    def mapper(self, _, line):
        # Ignore metadata / reports
        if 'info' in line and line['info']['message'] == 'Replay Request Completed':
            return

        # if any(rule['value'] == 'has:geo' line['gnip']['matching_rules']):
        if 'geo' in line and line['geo'].get('type') == 'Point':
            latitude, longitude = line['geo']['coordinates']
            for feature in self.feature_collection['features']:
                if bbox_contains(feature['bbox'], longitude, latitude):
                    yield feature['properties']['name'], line


if __name__ == '__main__':
    # Maybe run the whole thing in a try-catch-finally with counters for error logging?
    # might make it easier to debug than pulling down the whole bucket of attempts and
    # browsing through the stderr files to find the tracebacks
    # http://pythonhosted.org/mrjob/guides/writing-mrjobs.html#counters
    GeoExtract.run()
