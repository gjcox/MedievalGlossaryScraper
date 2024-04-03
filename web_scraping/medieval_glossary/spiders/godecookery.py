import logging
import re
import scrapy

from typing import Any, Generator

from scrapy.http import Response

from medieval_glossary.util import matches_plural_pattern, get_singular, get_plural, \
    matches_optional_pattern, get_with_optional, get_without_optional

GLOSSARY_ROOT_URL = "http://www.godecookery.com/glossary/glossary.htm"
GLOSSARY_PATTERN = re.compile(r"gloss\w.htm")
HTML_TAG_PATTERN = re.compile(r"<.*?>")
NEWLINE_PATTERN = re.compile(r"\n")
AMPERSAND_PATTERN = re.compile(r"&amp;")
DOUBLE_SPACE_PATTERN = re.compile(r"\s\s+")

class GodeCookerySpider(scrapy.Spider):
    name = "godecookeryglossary"
    allowed_domains = ["godecookery.com"]
    start_urls = [GLOSSARY_ROOT_URL]

    def clean_list_item(self, list_item: str) -> str:
        clean_html = re.sub(HTML_TAG_PATTERN, "", list_item)
        no_line_breaks = re.sub(NEWLINE_PATTERN, " ", clean_html)
        no_amberspand = re.sub(AMPERSAND_PATTERN, "and", no_line_breaks)
        no_double_space = re.sub(DOUBLE_SPACE_PATTERN, " ", no_amberspand)
        return no_double_space.strip()

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
            entries = map(self.clean_list_item, \
                             response.xpath("//li[1]").getall())
            
            for entry in entries:
                yield from self.split_entry_by_plaintext(entry)

            