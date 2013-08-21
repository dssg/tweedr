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


class a131709_datasource(CSVDatasouce):
    '''
    Counts:

     94 Other
    265 Informative (Direct)
    469 Informative (Indirect)
    762 Informative (Direct or Indirect)
    794 Personal only
    '''
    filepath = globfirst('**/a131709.csv', root=corpora_root)
    label_column = 'choose_one'
    text_column = 'tweet'


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


class a122047_datasource(CSVDatasouce):
    '''
    Counts:

      3 A shelter is open or available
     27 A siren has been heard
     99 A tornado sighting/touchdown has been reported
    102 Other
    207 A tornado/thunderstorm warning has been issued or has been lifted
    '''
    filepath = globfirst('**/a122047.csv', root=corpora_root)
    label_column = 'type_of_advice_or_caution'
    text_column = 'text'


class a126730_datasource(CSVDatasouce):
    '''
    Counts:

     1 Both people and infrastructure
     1 People: injured
     2 People: injured and dead
    12 Not damage-related
    17 Infrastructure (building, bridge, road, etc.) damaged
    47 Not specified (maybe people or infrastructure)
    58 People: dead
    '''
    filepath = globfirst('**/a126730.csv', root=corpora_root)
    label_column = 'people_or_infrastructure'
    text_column = 'text'


class a126728_datasource(CSVDatasouce):
    '''
    Counts:

      2 Discount (rebate/special offer)
      3 Blood
      3 Equipment (machine/generator/pump/etc.)
      6 Food
      7 Shelter
     11 Volunteers/work
     53 Money
    119 Other, or not specified
    '''
    filepath = globfirst('**/a126728.csv', root=corpora_root)
    label_column = 'type_of_donation'
    text_column = 'text'


if __name__ == '__main__':
    for label, text in a121571_datasource():
        print label, '\t', text
