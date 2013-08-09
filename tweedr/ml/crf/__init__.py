import crfsuite


class ItemSequence(crfsuite.ItemSequence):
    def __init__(self, features_iter):
        '''Create new ItemSequence, typedef std::vector<Item> based on the
        given iterable of iterable of 2-tuples or strings'''
        super(ItemSequence, self).__init__()
        self.append_raw(features_iter)

    def append_raw(self, features_iter):
        '''
        @features_iter is an iterable of iterables, of tuples or strings.
            type: [[(str, float) | str]], where [] is an iterable
        '''
        for features in features_iter:
            item = crfsuite.Item()
            for feature in features:
                if isinstance(feature, tuple):
                    attribute = crfsuite.Attribute(*feature)
                else:
                    attribute = crfsuite.Attribute(feature)
                item.append(attribute)
            self.append(item)
