import scrapy

from typing import List

from medieval_glossary.glossarybuilding.glossary import GlossaryEntry, Meaning
from medieval_glossary.glossarybuilding.util import get_singular, get_plural, object_to_dict
from medieval_glossary.spiders.medievalcookery import SPIDER_NAME as MC_SPIDER_NAME
from medieval_glossary.spiders.godecookery import SPIDER_NAME as GC_SPIDER_NAME

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class MedievalGlossaryPipeline:
    def split_meaning(self, meaning: str, is_plural: bool | None) -> tuple[str, str | None]:
        [substitution, *note_wrapper] = meaning.split(",", 1)
        
        # unwrap note if it exists 
        if note_wrapper:
            note = note_wrapper[0] 
        else:
            note = None
        
        # change substitution text to match plaintext pluralisation as needed
        if is_plural:
            substitution = get_plural(substitution)
        # N.B. use "is False" to account for use of None
        elif is_plural is False:
            substitution = get_singular(substitution)
        
        return (substitution, note)

    def process_item(self, item: dict[str, List[str], bool], spider: scrapy.Spider):
        entry = GlossaryEntry(item['plaintext'])
        if spider.name == GC_SPIDER_NAME:
            for meaning in item['meanings']:
                substitution, note = self.split_meaning(meaning, item['plural'])
                entry.add_meaning(Meaning(substitution, note))
        elif spider.name == MC_SPIDER_NAME:
            try:
                entry.set_synonym_of(item['synonymOf'])
            except KeyError:
                entry.add_meaning(Meaning(item['substitution'], item['note']))
        return object_to_dict(entry)
