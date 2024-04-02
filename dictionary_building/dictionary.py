import json
import logging
from typing import List
logger = logging.getLogger(__name__)

def check_sentence_counts(path: str, corpus: List[object]):
    for i, recipe in enumerate(corpus): 
        n_sentences_original = len(recipe['original_recipe'].split("."))
        n_sentences_translation = len(recipe['gode_cookery_translation'].split('.'))
        if n_sentences_original != n_sentences_translation:
            logger.info(f"Inconsistent sentence counts | "
                        f"line {i+1} of {path} | "
                        f"{n_sentences_original} vs {n_sentences_translation}.")

def find_faults_in_corpus(path: str):
    with open(path, 'r') as recipes_file:
        json_list = list(recipes_file)
    corpus = [json.loads(json_str) for json_str in json_list if json_str[:2] != "//"] 
    check_sentence_counts(path, corpus)
    

def main():
    logging.basicConfig(filename='dictionary.log', level=logging.INFO)
    find_faults_in_corpus('resources/recipes.jsonl')


if __name__ =='__main__':
    main()