positive_examples_file_path = 'data/MGI_Geno_Disease.rpt'
negative_examples_file_path = 'data/MGI_Geno_NotDisease.rpt'

positive_examples_rdf_file_path = 'data/mgi_geno_disease.ttl'
negative_examples_rdf_file_path = 'data/mgi_geno_notdisease.ttl'

diabetes_id = '222100'

# prefixes
prefix_mp = 'http://purl.obolibrary.org/obo/'
prefix_allelic_info_resource = 'http://dl-learner.org/smallis/allelic_info'

# uris
uri_has_phenotype = 'http://dl-learner.org/smallis/has_phenotype'
uri_allelic_composition = 'http://dl-learner.org/smallis/allelic_composition'
uri_background_strain = 'http://dl-learner.org/smallis/background_strain'
uri_example_class = 'http://dl-learner.org/smallis/Allelic_info'

# CSV column positions start with 0!!!
csv_col_pos_allelic_composition = 0
csv_col_pos_background_strain = 3
csv_col_pos_class_id = 4

csv_delimiter = '\t'