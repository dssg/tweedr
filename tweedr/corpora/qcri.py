import os
import csv
from tweedr.corpora import DatasourceI
from tweedr.lib import globfirst

corpora_root = os.path.expanduser(os.environ.get('CORPORA', '~/corpora'))


class CSVDatasouce(DatasourceI):
    filepath = None
    label_column = 'category'
    text_column = 'text'

    def __iter__(self):
        with open(self.filepath) as fp:
            for row in csv.DictReader(fp):
                yield row[self.label_column], row[self.text_column]


class a121571_datasource(CSVDatasouce):
    '''
    Counts:

     46 People missing, found or seen
    130 Unknown
    137 Casualties and damage
    204 Donations of money, goods or services
    280 Information source
    436 Caution and advice
    '''
    # TODO: come up with a better name
    filepath = globfirst('**/a121571.csv', root=corpora_root)
    label_column = 'choose_one'
    text_column = 'text'


if __name__ == '__main__':
    for label, text in a121571_datasource():
        print label, '\t', text
