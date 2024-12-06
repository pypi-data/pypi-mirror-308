# Inside BOOK_NLP_fr/__init__.py
print("BOOK_NLP_fr package loaded successfully.")

import pandas as pd
import pkg_resources

from .BOOKNLP_fr_number import assign_number_to_PER_entities
from .BOOKNLP_fr_gender import assign_gender_to_PER_entities


def add_mention_number_and_gender_infos(entities_df):
    # Locate the CSV file within the package
    insee_path = pkg_resources.resource_filename('BOOK_NLP_fr', 'data/insee_names_fr_1900_2023.csv')

    entities_df['number'] = assign_number_to_PER_entities(entities_df)['number']
    entities_df['gender'] = assign_gender_to_PER_entities(entities_df, insee_path=insee_path)['gender']
    return entities_df

from .BookNLP_fr import (load_text_file, save_text_file, save_tokens_df, load_tokens_df, save_entities_df, load_entities_df,
                        load_spacy_model, clean_text, generate_tokens_df, 
                        load_mentions_detection_models, predict_entities_from_tokens_df,
                        load_tokenizer_and_embedding_model, get_embedding_tensor_from_tokens_df,
                        get_mentions_embeddings,
                        add_infos_to_entities,
                        initialize_gold_coreference_matrix_from_entities_df,
                        extract_mentions_and_links_from_coreference_matrix, coreference_resolution_metrics,
                        initialize_mention_pairs_df, generate_mention_pairs_features_array, get_mention_pairs_gold_labels,
                        generate_coreference_resolution_training_dict, generate_split_data, get_mention_pairs_coreference_predictions,
                        DataGenerator, training_model)




