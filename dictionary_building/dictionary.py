import json
import logging
from typing import List
logger = logging.getLogger(__name__)

def check_sentence_counts(path: str, corpus: List[object]) -> bool:
    consistent_sentence_counts = True
    for i, recipe in enumerate(corpus): 
        n_sentences_original = len(recipe['original_recipe'].split("."))
        n_sentences_translation = len(recipe['gode_cookery_translation'].split('.'))
        if n_sentences_original != n_sentences_translation:
            logger.info(f"Inconsistent sentence counts | "
                        f"line {i+1} of {path} | "
                        f"{n_sentences_original} vs {n_sentences_translation}.")
            consistent_sentence_counts = False
    return consistent_sentence_counts

def check_word_counts(path: str, corpus: List[object]):
    consistent_word_counts = True
    for i, recipe in enumerate(corpus): 
        word_counts_original = list(map(lambda s: len(s.split(" ")), \
                                    recipe['original_recipe'].split("."))) 
        word_counts_translation = list(map(lambda s: len(s.split(" ")), \
                                       recipe['gode_cookery_translation'].split("."))) 
        for j, word_counts in enumerate(list(zip(word_counts_original, \
                                                 word_counts_translation))):
            if word_counts[0] != word_counts[1]:
                logger.info(f"Inconsistent word counts | "
                            f"line {i+1} of {path} | "
                            f"sentence {j+1} | "
                            f"{word_counts[0]} vs {word_counts[1]}.")
                consistent_word_counts = False  
    return consistent_word_counts


def find_faults_in_corpus(path: str):
    with open(path, 'r') as recipes_file:
        json_list = list(recipes_file)
    corpus = [json.loads(json_str) for json_str in json_list if json_str[:2] != "//"] 
    check_sentence_counts(path, corpus) and \
        check_word_counts(path, corpus)


def main():
    logging.basicConfig(filename='dictionary.log', level=logging.INFO)
    find_faults_in_corpus('resources/recipes.jsonl')


if __name__ =='__main__':
    main()