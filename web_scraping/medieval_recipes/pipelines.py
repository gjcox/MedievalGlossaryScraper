# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re 

# useful for handling different item types with a single interface
import scrapy

almost_roman_numerals_pattern = r"\.?[iljvx]+\.?"
recipe_prefixes = [almost_roman_numerals_pattern, r"\d+\.?", r".*¶"]

def clean_medieval_recipe(recipe: str) -> str:
    cleaned_recipe = recipe.strip()
    # remove prefix 
    for prefix in recipe_prefixes:
        cleaned_recipe = re.sub("^" + prefix, "", cleaned_recipe)
    return clean_recipe(cleaned_recipe)

def clean_recipe(recipe: str) -> str: 
    # remove newline characters 
    cleaned_recipe = recipe.replace("\n", " ")
    # remove slashes
    cleaned_recipe = cleaned_recipe.replace(" /", ".")
    return cleaned_recipe.strip()

class MedievalRecipeCleanerPipeline:
    def process_item(self, item: {str, str}, spider: scrapy.Spider):
        original_recipe = clean_medieval_recipe(item['original_recipe'])
        gode_cookery_translation = clean_recipe(item['gode_cookery_translation'])
        return {
            **item, 
            'original_recipe': original_recipe,
            'gode_cookery_translation': gode_cookery_translation, 
        }

