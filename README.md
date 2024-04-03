# MedievalGlossaryScraper

This is a web scraper used to build a glossary of terms for simple word-for-word translation of medieval recipes. The web scraper is built with the [scrapy library](https://scrapy.org/) for Python and the glossary is output as an unordered JSON lines file (resources/glossary.jsonl). 

## Credits 

The glossary is scraped from [Gode Cookery's Glossary of Medieval Cooking Terms](http://www.godecookery.com/glossary/glossary.htm) by James L. Matterer. I may expand this with other glossaries in future. 

## How to Use

The output glossary is included in this repository so it is likely unnecessary to clone the codebase, but if desirable then use the requirements document to install the required Python libraries, and run the scraper from within the web_scraping directory with:

    scrapy crawl godecookeryglossary

### Output Format 

Glossary entries are structured as a one-to-many mapping from medieval terms to modern words that can be substituted in their place. These substitutions can have notes attached, but the notes are not further broken up. 

The glossary entries are not perfect as the formatting of the web pages they are scraped from is not entirely consistent. For example, sometimes something that I would want to class as a note will appear as an alternate substitution instead. I may manually correct these in future. 