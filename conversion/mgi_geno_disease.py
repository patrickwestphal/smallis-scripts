#!/usr/bin/env python

import csv

from rdflib import Graph, URIRef, Literal, BNode
from rdflib import RDF, OWL

import mgi_geno_disease_conf as conf

ID_COUNTER = 0

# - extract all 1st and 4th column values (allelic composition plus background
#   strain) of lines containing “222100” (diabetes) in the last column into a
#   set S (for the first file this will result in the set of positive examples
#   and for the second file the set of negative examples)
# - extract all lines containing an element of S for each line: if the tuple
#   consisting of first and fourth column is $x and the 5th column is $y then
#   generate a triple $x rdf:type $y (it should be something like
#   (Ednra<tm1Ywa>/Ednra<tm1Ywa>, 129S/SvEv) rdf:type MP:0001560)

def get_examples_and_info(examples_file_path, csv_delimiter):
    example_info = set()
    examples = []

    with open(examples_file_path) as f:
        csv_reader = csv.reader(f, delimiter=csv_delimiter)

        for fields in csv_reader:
            examples.append(fields)

            if fields[-1] == conf.diabetes_id:
                # add allelic composition/background strain pair to sample info
                example_info.add((fields[conf.csv_col_allelic_composition],
                                  fields[conf.csv_col_background_strain]))

    return examples, example_info

def _id2cls(cls_id):
    return conf.prefix_mp + cls_id.replace(':', '_')

def _allelic_info_uri(attr_fields):
    global ID_COUNTER
    ID_COUNTER += 1
    return conf.prefix_allelic_info_resource + '%05i' % ID_COUNTER

def _add_class_link(graph, subject, cls):
    # add s rdf:type has-phenotype some MP:9876543
    bCls = BNode()
    bRestriction = BNode()

    graph.add((subject, RDF.type, bCls))
    graph.add((bCls, OWL.equivalentClass, bRestriction))
    graph.add((bRestriction, RDF.type, OWL.Restriction))
    graph.add((bRestriction, OWL.onProperty, URIRef(conf.uri_has_phenotype)))
    graph.add((bRestriction, OWL.someValuesFrom, cls))

def _add_allelic_info_literals(graph, subject, allelic_info):
    allelic_composition, bckgrnd_strain = allelic_info
    ac_literal = Literal(allelic_composition)
    bs_literal = Literal(bckgrnd_strain)

    graph.add((subject, URIRef(conf.uri_allelic_composition), ac_literal))
    graph.add((subject, URIRef(conf.uri_background_strain), bs_literal))

def _add_example_class(graph, subject):
    graph.add((subject, RDF.type, URIRef(conf.uri_example_class)))

def build_rdf(examples, example_info):
    g = Graph()

    for example in examples:
        # create allelic comp/background strain info
        ai_bs_info = (example[conf.csv_col_allelic_composition],
                      example[conf.csv_col_background_strain])
        if ai_bs_info in example_info:
            s = URIRef(_allelic_info_uri(example))

            cls = URIRef(_id2cls(example[conf.csv_col_class_id]))
            _add_class_link(g, s, cls)
            _add_allelic_info_literals(g, s, ai_bs_info)
            _add_example_class(g, s)

    return g

def run():
    # positive examples
    pos_examples, pos_examples_diabetes_info = get_examples_and_info(
        conf.positive_examples_file_path, conf.csv_delimiter)

    g_pos = build_rdf(pos_examples, pos_examples_diabetes_info)

    with open(conf.positive_examples_rdf_file_path, 'wb') as f:
        f.write(g_pos.serialize(format='turtle'))

    # negative examples
    neg_examples, neg_examples_diabetes_info = get_examples_and_info(
        conf.negative_examples_file_path, conf.csv_delimiter)

    g_neg = build_rdf(neg_examples, neg_examples_diabetes_info)

    with open(conf.negative_examples_rdf_file_path, 'wb') as f:
        f.write(g_neg.serialize(format='turtle'))

if __name__ == '__main__':
    run()