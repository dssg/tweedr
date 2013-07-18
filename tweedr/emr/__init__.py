import ujson
from mrjob.protocol import _ClassBasedKeyCachingProtocol


class UltraJSONProtocol(_ClassBasedKeyCachingProtocol):
    @classmethod
    def load_from_string(cls, value):
        return ujson.loads(value)

    @classmethod
    def dump_to_string(cls, value):
        return ujson.dumps(value)


class UltraJSONValueProtocol(object):
    @classmethod
    def read(cls, line):
        return (None, ujson.loads(line))

    @classmethod
    def write(cls, key, value):
        return ujson.dumps(value)
