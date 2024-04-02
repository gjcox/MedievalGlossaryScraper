import logging
import re
from typing import Any

import scrapy
from scrapy.http import Response

class GodeCookerySpider(scrapy.Spider):
    name = "godecookery"
    allowed_domains = ["godecookery.com"]
    start_urls = ["http://www.godecookery.com/mtrans/mtrans.htm"]

    def parse(self, response: Response) -> Any:
        if response.url == "http://www.godecookery.com/mtrans/mtrans.htm":
            # follow other URLs from directory page 
            anchors = response.xpath('//a/@href')
            recipe_anchors = [anchor for anchor in anchors if re.findall(r"mtrans/mtrans\d+\.htm", anchor.get())]
            yield from response.follow_all(recipe_anchors, callback=self.parse)

        elif re.findall(r"/mtrans/mtrans\d+\.htm", response.url):
            # extract text 
            try:
                yield {
                    'original_recipe': response.xpath("//td/p[6]/b/text()").get(),
                    'citation': " ".join(response.xpath("//td/p[7]//text()").getall()).replace("\n", " "),
                    'gode_cookery_translation': response.xpath("//td/p[10]/b/text()").get(),
                    'url': response.url,
                }

            except:
                self.log(f"Something went wrong. {response.url} may not have the expected page layout", logging.ERROR)
