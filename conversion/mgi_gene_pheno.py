#!/usr/bin/env python

import mgi_gene_pheno_conf as conf

# - download ftp.informatics.jax.org/pub/reports/MGI_GenePheno.rpt 
# - extract all 1st and 4th column values (allelic composition plus background
#   strain) of lines containing MP:0004031 (theoretically also its subclasses)
#   into a set S (this is the set of positive instances)
# - extract the set N of 1st and 4th column values (allelic composition plus
#   background strain) such that the tuple consisting of 1st and 4th column
#   values is not in S; randomly select a subset N’ of N such that size of N’
#   is equal (2x, 10x the size) to size S. N’ is the set of negative instances.
# - for each line: if the tuple consisting of first and fourth column is $x
#   and the 5th column is $y then generate a triple $x rdf:type $y (it should
#   be something like
#   (Ednra<tm1Ywa>/Ednra<tm1Ywa>, 129S/SvEv) rdf:type MP:0001560)
#   --> the result is one file in the DL-Learner background knowledge (binding
#       the examples to the MP ontology)
# - <extract negative examples>
# - the second and third file are mp.owl and mp-equiv-axioms.obo


def run():
    # read positive example data
    # convert positive example data to RDF
    # read negative example data
    # convert negative example data to RDF
    pass

if __name__ == '__main__':
    run()