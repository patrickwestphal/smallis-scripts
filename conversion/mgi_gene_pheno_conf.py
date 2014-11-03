positive_examples_file_path = 'data/MGI_GenePheno.rpt'
positive_examples_rdf_file_path = 'data/mgi_gene_pheno_pos.ttl'

positive_examples_pheno_id = 'MP:0004031'
negative_examples_file_path = 'data/Normal_MPannot_V2.csv'

negative_examples_rdf_file_path = 'data/mgi_gene_pheno_neg.ttl'


# csv
csv_pos_col_allelic_composition = 0
csv_pos_col_background_strain = 3
csv_pos_col_mp_id = 4
csv_pos_delimiter = '\t'
csv_neg_col_mp_id = 1
csv_neg_header_line = True
csv_neg_delimiter = '\t'

# prefixes
prefix_mp = 'http://purl.obolibrary.org/obo/'
prefix_allelic_info_resource = 'http://dl-learner.org/smallis/allelic_info'

# uris
uri_has_phenotype = 'http://dl-learner.org/smallis/has_phenotype'
uri_allelic_composition = 'http://dl-learner.org/smallis/allelic_composition'
uri_background_strain = 'http://dl-learner.org/smallis/background_strain'
uri_example_class = 'http://dl-learner.org/smallis/Allelic_info'