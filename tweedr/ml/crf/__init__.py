from tweedr.lib.text import utf8str
import crfsuite


class ItemSequence(crfsuite.ItemSequence):
    def __init__(self, features_iter, check=False):
        '''Create new ItemSequence, typedef std::vector<Item> based on the
        given iterable of iterable of 2-tuples or strings.
        If check=True, any unicode present in the given features_iter
        will be encoded into a bytestring as utf8.'''
        super(ItemSequence, self).__init__()
        self.append_raw(features_iter, check=check)

    def append_raw(self, features_iter, check=False):
        '''
        @features_iter is an iterable of iterables, of tuples or strings.
            type: [[(str, float) | str]], where [] is an iterable
        '''
        for features in features_iter:
            if check:
                features = map(utf8str, features)
            item = crfsuite.Item()
            for feature in features:
                if isinstance(feature, tuple):
                    attribute = crfsuite.Attribute(*feature)
                else:
                    attribute = crfsuite.Attribute(feature)
                item.append(attribute)
            self.append(item)
