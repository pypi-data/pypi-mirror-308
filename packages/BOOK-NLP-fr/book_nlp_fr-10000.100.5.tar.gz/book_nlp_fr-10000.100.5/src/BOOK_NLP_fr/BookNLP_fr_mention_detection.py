import pandas as pd

## Mentions Detection - Generate entities_df from tokens_df
# %%
from flair.models import SequenceTagger
from flair.data import Sentence

def load_mentions_detection_models(models_paths=['AntoineBourgois/BookNLP_fr_mentions_detection_nested_level_0']):
    flair_models = [SequenceTagger.load(model_path) for model_path in models_paths]
    return flair_models

def combine_predicted_entities(predicted_entities_dfs):
    all_predicted_entities = predicted_entities_dfs[0]
    for new_predicted_entities in predicted_entities_dfs[1:]:
        new_predicted_entities['is_cutting'] = False
        for index, row in new_predicted_entities.iterrows():
            start_token, end_token = row['start_token'], row['end_token']
            cut_predicted_entities = all_predicted_entities[
                ((all_predicted_entities['start_token'] < start_token) & (
                            (all_predicted_entities['end_token'] > start_token) & (
                                all_predicted_entities['end_token'] < end_token)))
                | ((all_predicted_entities['end_token'] > end_token) & (
                            (all_predicted_entities['start_token'] > start_token) & (
                                all_predicted_entities['start_token'] < end_token)))
                | ((all_predicted_entities['start_token'] == start_token) & (
                            all_predicted_entities['end_token'] == end_token))
                ]
            if not cut_predicted_entities.empty:
                new_predicted_entities.loc[index, 'is_cutting'] = True

        new_predicted_entities = new_predicted_entities[new_predicted_entities['is_cutting'] == False].drop(
            'is_cutting', axis=1)
        all_predicted_entities = pd.concat([all_predicted_entities, new_predicted_entities])
        all_predicted_entities = all_predicted_entities.drop_duplicates()
        all_predicted_entities = all_predicted_entities.sort_values(['start_token', 'end_token'],
                                                                    ascending=True).reset_index(drop=True)

    return all_predicted_entities

def predict_entities_from_tokens_df(tokens_df, flair_models=None, batch_size=16, max_tokens=250, verbose=True):
    predicted_entities_dfs = []
    sentences = []

    for sentence_id, sentence_df in tokens_df.groupby('sentence_ID'):
        words = sentence_df['word'].tolist()
        # Split into chunks of max_tokens using list comprehension
        chunks = [words[i:i + max_tokens] for i in range(0, len(words), max_tokens)]

        # Convert each chunk into a Sentence object and add to the list
        sentences.extend(Sentence(chunk, use_tokenizer=False) for chunk in chunks)

    for model in flair_models:
        # predict tags
        model.predict(sentences, verbose=verbose, mini_batch_size=batch_size)

        token_offset = 0
        predicted_mentions_dict = []
        for sentence in sentences:
            for mention in sentence.get_spans():
                start_token = token_offset + mention[0].idx - 1
                end_token = token_offset + mention[-1].idx - 1
                confidence = mention.score
                predicted_mentions_dict.append(
                    {'start_token': start_token, 'end_token': end_token, 'text': mention.text, 'cat': mention.tag,
                     'confidence': confidence})
            token_offset += len(sentence)

        predicted_entities_df = pd.DataFrame(predicted_mentions_dict)
        predicted_entities_dfs.append(predicted_entities_df)

    all_predicted_entities = combine_predicted_entities(predicted_entities_dfs)
    return all_predicted_entities