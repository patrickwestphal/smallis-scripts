#!/usr/bin/env python

import csv

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
_log = logging.getLogger()

from urllib.parse import quote

from rdflib import Graph
from rdflib import URIRef
from rdflib import Literal
from rdflib import RDFS, RDF


INPUT_FILE_PATH = 'data/MGI_PhenotypicAllele.rpt'
OUTPUT_FILE_PATH = 'mgi_phenotypic_alleles.nt'
DELIMITER = '\t'
COMMENT_CHAR = '#'
DEFAULT_PREFIX = 'dl-learner.org/smallis/'
MGI_PREFIX = 'www.informatics.jax.org/allele/'
MGI_MARKER_PREFIX = 'http://www.informatics.jax.org/marker/'
SYN_PROPERTY_URI = 'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym'

# helper functions
def _extract_mp_uris(field_val):
    prefix = 'http://purl.obolibrary.org/obo/'
    ids = field_val.split(',')

    return [prefix + id_.replace(':', '_') for id_ in ids]

FIELD_MAPPINGS = [
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'allele_symbol'), 'o_type': 'plain'},
    {'skip': False, 'p': RDFS.label, 'o_type': 'plain'},
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'allele_type'), 'o_type': 'uri', 'prefix': DEFAULT_PREFIX},
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'allele_attribute'), 'o_type': 'plain'},
    {'skip': True},
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'marker'), 'o_type': 'uri', 'prefix': MGI_MARKER_PREFIX},
    {'skip': True},  # marker sybol -- should be linked to marker
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'marker_ref'), 'o_type': 'plain'},
    {'skip': False, 'p': URIRef(DEFAULT_PREFIX + 'marker_ensemble_id'), 'o_type': 'plain'},
    {'skip': False, 'p': RDF.type, 'o_type': 'uri', 'o_func': _extract_mp_uris},
    {'skip': False, 'p': URIRef(SYN_PROPERTY_URI), 'o_type': 'plain'},
    {'skip': True},
    {'skip': True}
]

def run():
    g = parse_graph()
    with open(OUTPUT_FILE_PATH, 'wb') as f:
        f.write(g.serialize(format='nt'))


def parse_graph():
    g = Graph()

    with open(INPUT_FILE_PATH) as f:
        csv_reader = csv.reader(f, delimiter=DELIMITER)

        line_counter = 0
        for fields in csv_reader:
            line_counter += 1
            if line_counter % 1000 == 0:
                _log.debug('%i lines read' % line_counter)

            if len(fields) == 1 and fields[0].strip().startswith(COMMENT_CHAR):
                continue

            mgi_id = fields[0]
            if mgi_id.startswith('MGI'):
                s = g.resource(MGI_PREFIX + quote(mgi_id))

                for i in range(1, len(fields)):
                    field_val = fields[i]

                    if not field_val.strip() or FIELD_MAPPINGS[i-1]['skip'] == True:
                        continue

                    type = FIELD_MAPPINGS[i-1]['o_type']

                    p = FIELD_MAPPINGS[i-1]['p']

                    if type == 'plain':
                        o = Literal(field_val)
                        s.add(p, o)

                    elif type == 'uri':
                        if FIELD_MAPPINGS[i-1].get('o_func'):
                            func = FIELD_MAPPINGS[i-1]['o_func']
                            uris = func(field_val)
                            for uri_str in uris:
                                o = URIRef(uri_str)
                                s.add(p, o)

                        else:
                            o = URIRef(FIELD_MAPPINGS[i-1]['prefix'] + quote(field_val))
                            s.add(p, o)

                    # import pdb; pdb.set_trace()
                    # pass
    # import pdb; pdb.set_trace()
    return g

if __name__ == '__main__':
    run()
