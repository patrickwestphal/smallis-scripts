#!/usr/bin/env python

import csv

from rdflib import Graph, BNode, Literal
from rdflib import URIRef
from rdflib import RDF, OWL

import mgi_gene_pheno_conf as conf

# - download ftp.informatics.jax.org/pub/reports/MGI_GenePheno.rpt 
# - extract all 1st and 4th column values (allelic composition plus background
#   strain) of lines containing MP:0004031 (theoretically also its subclasses)
#   into a set S (this is the set of positive instances)
# - for each line: if the tuple consisting of first and fourth column is $x
#   and the 5th column is $y then generate a triple $x rdf:type $y (it should
#   be something like
#   (Ednra<tm1Ywa>/Ednra<tm1Ywa>, 129S/SvEv) rdf:type MP:0001560)
# - <extract negative examples>
#   --> the result is one file in the DL-Learner background knowledge (binding
#       the examples to the MP ontology)
# - the second and third file are mp.owl and mp-equiv-axioms.obo

ID_COUNTER = 0

def get_positive_examples_and_info():
    """structure of the MGI_GenePheno.rpt file (positive examples) "Genotypes
    and Mammalian Phenotype Annotations for Marker Type Genes excluding
    conditional mutations"

    #0 Allelic Composition (e.g. Rb1<tm1Tyj>/Rb1<tm1Tyj>)
    #1 Allele Symbol(s) (e.g. Rb1<tm1Tyj>)
    #2 Allele ID(s) (e.g. MGI:1857242)
    #3 Genetic Background (e.g. "involves: 129S2/SvPas")
    #4 Mammalian Phenotype ID (e.g. MP:0000600)
    #5 PubMed ID (e.g. 12529408)
    #6 MGI Marker Accession ID (comma-delimited) (e.g. MGI:97874)
    #7 empty column
    #8 MGI Genotype Accession ID (comma-delimited) (e.g. MGI:2166359)
    """
    example_info = set()
    examples = []

    with open(conf.positive_examples_file_path) as f:
        csv_reader = csv.reader(f, delimiter=conf.positive_exmaples_csv_delimiter)

        for fields in csv_reader:
            examples.append(fields)

            if fields[4] == conf.positive_exmaples_pheno_id:
                # add allelic composition/background strain pair to sample info
                example_info.add((fields[conf.csv_col_pos_allelic_composition],
                                  fields[conf.csv_col_pos_background_strain]))

    return examples, example_info

def _allelic_info_uri(example):
    global ID_COUNTER
    ID_COUNTER += 1
    return conf.prefix_allelic_info_resource + '%05i' % ID_COUNTER

def _id2cls(cls_id):
    return conf.prefix_mp + cls_id.replace(':', '_')

def _add_allelic_info_literals(graph, subject, allelic_info):
    allelic_composition, bckgrnd_strain = allelic_info
    ac_literal = Literal(allelic_composition)
    bs_literal = Literal(bckgrnd_strain)

    graph.add((subject, URIRef(conf.uri_allelic_composition), ac_literal))
    graph.add((subject, URIRef(conf.uri_background_strain), bs_literal))

def _add_class_link(graph, subject, cls):
    # add s rdf:type has-phenotype some MP:9876543
    bCls = BNode()
    bRestriction = BNode()

    graph.add((subject, RDF.type, bCls))
    graph.add((bCls, OWL.equivalentClass, bRestriction))
    graph.add((bRestriction, RDF.type, OWL.Restriction))
    graph.add((bRestriction, OWL.onProperty, URIRef(conf.uri_has_phenotype)))
    graph.add((bRestriction, OWL.someValuesFrom, cls))

def _add_example_class(graph, subject):
    graph.add((subject, RDF.type, URIRef(conf.uri_example_class)))

def build_pos_rdf(examples, example_info):
    g = Graph()

    for example in examples:
        # create allelic comp/background strain info
        ai_bs_info = (example[conf.csv_col_pos_allelic_composition],
                      example[conf.csv_col_pos_background_strain])
        if ai_bs_info in example_info:
            s = URIRef(_allelic_info_uri(example))

            cls = URIRef(_id2cls(example[conf.csv_col_pos_mp_id]))
            _add_class_link(g, s, cls)
            _add_allelic_info_literals(g, s, ai_bs_info)
            _add_example_class(g, s)

    return g

def run():
    # read positive example data
    pos_examples, pos_examples_insulitis_info = get_positive_examples_and_info()

    # convert positive example data to RDF
    g_pos = build_pos_rdf(pos_examples, pos_examples_insulitis_info)

    # write result to file
    with open(conf.positive_examples_rdf_file_path, 'wb') as f:
        f.write(g_pos.serialize(format='turtle'))

    # read negative example data
    # convert negative example data to RDF
    pass

if __name__ == '__main__':
    run()