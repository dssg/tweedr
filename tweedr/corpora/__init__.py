class DatasourceI(object):
    '''As usual, a reference, as opposed to an interface you actually have to implement'''

    def __init__(self):
        pass

    def __iter__(self):
        '''This should yield tuples of label-document (basestring, basestring) pairs.'''
        raise NotImplementedError(__doc__)
