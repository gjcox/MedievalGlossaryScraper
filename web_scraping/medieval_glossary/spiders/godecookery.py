import logging
import re
import scrapy

from typing import Any, Generator

from scrapy.http import Response

from web_scraping.medieval_glossary.glossarybuilding.util import matches_plural_pattern, get_singular, get_plural, \
    matches_optional_pattern, get_with_optional, get_without_optional, clean_glossary_entry

SPIDER_NAME = "godecookeryglossary"
GLOSSARY_ROOT_URL = "http://www.godecookery.com/glossary/glossary.htm"
GLOSSARY_PATTERN = re.compile(r"gloss\w.htm")

class GodeCookerySpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = ["godecookery.com"]
    start_urls = [GLOSSARY_ROOT_URL]

    def split_entry_by_plaintext(self, list_item: str) -> Generator:
        try:
            [plaintexts, meanings] = map(lambda x: x.split(";"), \
                                        list_item.split(' - ', 1))
        except ValueError:
            self.log(f"\"{list_item}\" did not match \" - \" and could not be split", logging.WARNING)
            yield None
            return
        for plaintext in plaintexts:
            if matches_plural_pattern(plaintext):
                yield {
                    'plaintext': get_singular(plaintext),
                    'meanings': meanings, 
                    'plural': False
                    }
                yield { 
                    'plaintext': get_plural(plaintext),
                    'meanings': meanings, 
                    'plural': True
                    }
            elif matches_optional_pattern(plaintext):
                yield {
                    'plaintext': get_with_optional(plaintext),
                    'meanings': meanings, 
                    'plural': None
                    }
                yield { 
                    'plaintext': get_without_optional(plaintext),
                    'meanings': meanings, 
                    'plural': None
                    }
            else:
                yield {
                    'plaintext': plaintext, 
                    'meanings': meanings, 
                    'plural': None 
                    }

    def parse(self, response: Response) -> Any:
        if response.url == GLOSSARY_ROOT_URL:
            # follow other URLs from directory page 
            anchors = response.xpath('//a/@href')
            recipe_anchors = [anchor for anchor in anchors if \
                              re.findall(GLOSSARY_PATTERN, anchor.get())]
            yield from response.follow_all(recipe_anchors, callback=self.parse)

        elif re.findall(GLOSSARY_PATTERN, response.url):
            # extract entries
            entries = map(clean_glossary_entry, \
                             response.xpath("//li[1]").getall())
            
            for entry in entries:
                yield from self.split_entry_by_plaintext(entry)

            