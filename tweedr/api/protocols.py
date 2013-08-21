class StringProtocol(object):
    pass


class DictProtocol(object):
    pass


class TweetDictProtocol(DictProtocol):
    '''This merely asserts that the following fields will exist and have reasonable values:

        text: String
        id: String
        author: String
    '''
