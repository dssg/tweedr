import os
import requests
from tweedr.ml.spotlight import annotate
from tweedr.lib.text import zip_boundaries

spotlight_annotate_url = '%s/rest/annotate' % os.environ.get('SPOTLIGHT', 'http://spotlight.sztaki.hu:2222')


def get_pos(offset, document):
    doc_joined = " ".join(document)
    beginning = doc_joined[:offset]
    length = len(beginning.split(" ")) - 1
    return length


def features(document):
    doc_length = len(document)
    doc_joined = " ".join(document)
    positions = [[] for x in xrange(doc_length)]
    try:
        annotations = annotate('http://tweedr.dssg.io:2222/rest/annotate', doc_joined, confidence=0.4, support=20)
        for a in annotations:
            offset = a["offset"]
            type = a["types"]
            all_types = type.split(",")
            dbpedia_type = all_types[0]
            pos = get_pos(offset, document)
            db = str(dbpedia_type)
            positions[pos] = [db.upper()]
    except Exception:
        return positions
    return positions


def spotlight(document, confidence=0.1, support=10):
    document_string = u' '.join(document)
    r = requests.post(spotlight_annotate_url,
        headers=dict(Accept='application/json'),
        data=dict(text=document_string, confidence=confidence, support=support))
    Resources = r.json().get('Resources', [])
    for token, token_start, token_end in zip_boundaries(document):
        labels = []
        for Resource in Resources:
            entity_start = int(Resource['@offset'])
            entity_end = entity_start + len(Resource['@surfaceForm'])

            if entity_start <= token_start <= entity_end or entity_start <= token_end <= entity_end:
                entity_uri = Resource['@URI']
                entity_types = Resource['@types'].split(',')
                labels += [entity_uri] + entity_types
        yield labels
