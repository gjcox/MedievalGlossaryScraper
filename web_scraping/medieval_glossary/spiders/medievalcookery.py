import logging
import re
import scrapy

from typing import Any, Generator

from scrapy.http import Response

from medieval_glossary.glossarybuilding.util import clean_glossary_entry

SPIDER_NAME = "medievalcookeryglossary"
GLOSSARY_ROOT_URL = "https://medievalcookery.com/dictionary/"
GLOSSARY_PATTERN = re.compile(r"index.html\?[a-z]")

def split_mc_plaintexts(string: str):
    PATTERN = r"(?P<plaintext>(?:\w+\s)+)(?:\(also: )(?P<alt_plaintexts>(?:[\w\s]+(?:,\s)?)+)(?:\))"
    m = re.search(PATTERN, string)
    if m:
        plaintext = m.group('plaintext').strip()
        synonyms = m.group('alt_plaintexts').split(", ")
        return [plaintext, synonyms]
    else:
        return [string, []]

def split_mc_meaning(string: str):
    PATTERN = r"(?P<substitution>[^,\.\(]+)(?P<note>.*)"
    m = re.search(PATTERN, string)
    if m:
        substitution = m.group('substitution')
        substitution = substitution.strip(",. ")
        substitution = substitution.lower()

        note = m.group('note')
        note = note.strip(",. ")

        return [substitution, note]
    else:
        return [string, None]

class MedievalCookerySpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = ["medievalcookery.com"]
    start_urls = [GLOSSARY_ROOT_URL]

    def process_entry(self, list_item: str) -> Generator:
        try:
            [raw_plaintext, raw_meaning] = list_item.split(" : ", 1)
            [plaintext, synonyms] = split_mc_plaintexts(raw_plaintext)
            [substitution, note] = split_mc_meaning(raw_meaning)
            yield {
                'plaintext': plaintext,
                'substitution': substitution, 
                'note': note
            }
            for synonym in synonyms:
                yield {
                    'plaintext': synonym,
                    'synonymOf': plaintext, 
                }
        except ValueError:
            self.log(f"\"{list_item}\" could not be processed", logging.WARNING)
            yield None
            return

    def parse(self, response: Response) -> Any:
        if response.url == GLOSSARY_ROOT_URL:
            # follow other URLs from directory page 
            anchors = response.xpath('//a/@href')
            recipe_anchors = [anchor for anchor in anchors if \
                              re.findall(GLOSSARY_PATTERN, anchor.get())]
            yield from response.follow_all(recipe_anchors, callback=self.parse)

        elif re.findall(GLOSSARY_PATTERN, response.url):
            # extract entries
            entries = list(map(clean_glossary_entry, \
                             response.xpath("//a/p[@class='maintext']").getall()))
            
            for entry in entries:
                yield from self.process_entry(entry)
            