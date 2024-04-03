import re
import scrapy
import logging

from typing import Any

from scrapy.http import Response

GLOSSARY_ROOT_URL = "http://www.godecookery.com/glossary/glossary.htm"
GLOSSARY_PATTERN = re.compile(r"/glossary/gloss\w.htm")
HTML_TAG_PATTERN = re.compile(r"<.*?>")
NEWLINE_PATTERN = re.compile(r"\n")
AMPERSAND_PATTERN = re.compile(r"&amp;")
DOUBLE_SPACE_PATTERN = re.compile(r"\s\s+")

def cleanListItem(list_item: str) -> str:
    clean_html = re.sub(HTML_TAG_PATTERN, "", list_item)
    no_line_breaks = re.sub(NEWLINE_PATTERN, " ", clean_html)
    no_amberspand = re.sub(AMPERSAND_PATTERN, "and", no_line_breaks)
    no_double_space = re.sub(DOUBLE_SPACE_PATTERN, " ", no_amberspand)
    return no_double_space.strip()

class GodeCookerySpider(scrapy.Spider):
    name = "godecookeryglossary"
    allowed_domains = ["godecookery.com"]
    start_urls = ["http://www.godecookery.com/glossary/glossv.htm"]

    def parse(self, response: Response) -> Any:
        if response.url == GLOSSARY_ROOT_URL:
            # follow other URLs from directory page 
            anchors = response.xpath('//a/@href')
            recipe_anchors = [anchor for anchor in anchors if \
                              re.findall(GLOSSARY_PATTERN, anchor.get())]
            yield from response.follow_all(recipe_anchors, callback=self.parse)

        elif re.findall(GLOSSARY_PATTERN, response.url):
            # extract entries
            entries = map(cleanListItem, \
                             response.xpath("//li[1]").getall())
            yield from list(map(lambda y: {'text': y}, entries))
            