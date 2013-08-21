from tweedr.api.protocols import DictProtocol


class Mapper(object):
    '''Passthrough / interface'''
    INPUT = DictProtocol
    OUTPUT = DictProtocol

    def __call__(self, dict_):
        return dict_
