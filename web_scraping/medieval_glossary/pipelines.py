import logging
import re
from typing import List
import scrapy

from medieval_glossary.util import PLURAL_PATTERN, get_singular, get_plural, object_to_dict
from medieval_glossary.glossarybuilding.glossary import \
                                                GlossaryEntry, Meaning
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from medieval_glossary.util import get_singular, get_plural, matches_plural_pattern

class MedievalGlossaryPipeline:
    def process_item(self, item: dict[str, List[str], bool], spider: scrapy.Spider):
        entry = GlossaryEntry(item['plaintext'])
        if item['plural'] is None:
            for meaning in item['meanings']:
                [substitution, *note] = meaning.split(",", 1)
                if note:
                    entry.add_meaning(Meaning(substitution, note[0]))
                else:
                    entry.add_meaning(Meaning(substitution))
            return object_to_dict(entry)
        else:
            raise scrapy.DropItem("TODO")
        #     elif matches_plural_pattern(substitution):

        # [plaintexts, meanings] = map(lambda x: x.split(";"), \
        #                              item['text'].split(' - ', 1))
        # for plaintext in plaintexts:
        #     plaintext_plural_match = re.search(plural_pattern, plaintext)
        #     if plaintext_plural_match:
        #         entry_sing = GlossaryEntry(getSingular(plaintext, plaintext_plural_match.group()))
        #         entry_plural = GlossaryEntry(getPlural(plaintext, plaintext_plural_match.group()))
        #     else:
        #         entry = GlossaryEntry(plaintext)

        #     for meaning in meanings: 
        #         [substitution, *note] = meaning.split(",", 1)
        #         sub_plural_match = re.search(plural_pattern, substitution)
        #         if plaintext_plural_match and sub_plural_match: 
        #             sub_sing = getSingular(substitution, sub_plural_match.group())
        #             sub_plural = getPlural(substitution, sub_plural_match.group())
        #             if note:
        #                 sing_meaning = Meaning(sub_sing, note[0])
        #                 plural_meaning = Meaning(sub_plural, note[0])
        #             else:
        #                 sing_meaning = Meaning(sub_sing)
        #                 plural_meaning = Meaning(sub_plural)
        #             entry_sing.add_meaning(sing_meaning)
        #             entry_plural.add_meaning(plural_meaning)
        #             yield vars(entry_sing)
        #             yield vars(entry_plural)
        #         else:
        #             if note:
        #                 entry.add_meaning(Meaning(substitution, note[0]))
        #             else:
        #                 entry.add_meaning(Meaning(substitution))
        #             yield vars(entry)
            
class YieldToReturnPipeline:
    def process_item(self, item: GlossaryEntry, spider: scrapy.Spider) -> GlossaryEntry:
        # spider.log(f"YieldToReturnPipeline received {item}", logging.INFO)
        return list(item)