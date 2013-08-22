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
    # from joplin/
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
    # from joplin/
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
    # from joplin/
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
    # from joplin/
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
    # from joplin/
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


class a122582_datasource(CSVDatasouce):
    # from joplin/
    '''
    Counts:

      4 Tune to this radio station (or: I am listening to this station)
     10 Watch this TV channel (or: I am watching this channel)
     33 None of the above
     35 Look at this photo or these photos
     58 Look at this video or these videos
    139 Look at this web site/page
    '''
    filepath = globfirst('**/a122582.csv', root=corpora_root)
    label_column = 'type_of_message'
    text_column = 'text'


class a143145_datasource(CSVDatasouce):
    # from sandy/
    '''
    Counts:

     78 Informative (Direct)
     79 Informative (Direct or Indirect)
    161 Other
    296 Personal Only
    386 Informative (Indirect)
    '''
    filepath = globfirst('**/a143145.csv', root=corpora_root)
    label_column = 'choose_one'
    text_column = 'tweet'


class a144267_datasource(CSVDatasouce):
    # from sandy/
    '''
    Counts:

     32 Donations of money, goods or services
     72 Information Source
    125 Unknown
    144 Caution and advice
    170 Casualties and damage
    '''
    filepath = globfirst('**/a144267.csv', root=corpora_root)
    label_column = 'choose_one'
    text_column = 'tweet'


class a146283_datasource(CSVDatasouce):
    # from sandy/
    '''
    Counts:

     6 A shelter is open or available
    20 A hurricane warning has been issued or has been lifted
    23 A hurricane sighting has been reported
    77 Other
    '''
    filepath = globfirst('**/a146283.csv', root=corpora_root)
    label_column = 'type_of_advice_or_caution'
    text_column = 'tweet'


class a146281_datasource(CSVDatasouce):
    # from sandy/
    '''
    Counts:

     1 People: injured
     3 People: injured and dead
    12 Not specified (maybe people or infrastructure)
    13 Both people and infrastructure
    16 Not damage-related
    34 People: dead
    91 Infrastructure (building, bridge, road, etc.) damage
    '''
    filepath = globfirst('**/a146281.csv', root=corpora_root)
    label_column = 'people_or_infrastructure'
    text_column = 'tweet'


if __name__ == '__main__':
    for label, text in a121571_datasource():
        print label, '\t', text
