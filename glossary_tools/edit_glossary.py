import sys, os, argparse, json, io

# ''' I am aware this is quite hacky, but to my understanding scrapy makes
#     temporary virtual filespaces when it runs, so it is easier to jankily
#     import modules from the web_scraping package than into the web_scraping
#     package. Additionally, while this might be a brittle solution I only 
#     intend this code to run on my machine so flexibility is not a high 
#     priority. '''
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import web_scraping.medieval_glossary.glossarybuilding.glossary as glossary
# import web_scraping.medieval_glossary.glossarybuilding.util as glosutils

def synonyms(source: io.TextIOWrapper, output: io.TextIOWrapper):
    # Load JSON entries from source
    entry_list = [json.loads(line) for line in source]

    # Track occurrences of meanings to find synonyms
    # ... and replace 'meanings' key with 'synonymOf' key as appropriate 
    meanings_tracker = {}
    for entry in entry_list:
        if 'meanings' in entry:
            meanings_str = str(entry['meanings'])
            try:
                entry['synonymOf'] = meanings_tracker[meanings_str]['origin']
                entry.pop('meanings', None)
            except KeyError:
                meanings_tracker[meanings_str] = {
                    'origin': entry['plaintext'],
                    'count': 0, 
                }
        # else: likely already a synonymOf _
    
    # Write processed entries to output file
    output.writelines(json.dumps(entry, ensure_ascii=False) + '\n' for entry in entry_list)
 

def alphabetise(source: io.TextIOWrapper, output: io.TextIOWrapper):
    # Load JSON entries from source
    entry_list = [json.loads(line) for line in source]
    # Sort entries by plaintext 
    entry_list.sort(key=lambda entry : entry['plaintext'])
    # Write processed entries to output file
    output.writelines(json.dumps(entry, ensure_ascii=False) + '\n' for entry in entry_list)


tasks = {
    'alphabetise': alphabetise,
    'synonyms': synonyms,
}


def main():
    parser = argparse.ArgumentParser(description='Process a JSON-lines glossary file.')
    parser.add_argument("task", choices=tasks.keys())
    parser.add_argument("source", type=argparse.FileType('r', encoding='UTF-8'), 
                        help="the current glossary file")
    parser.add_argument("output", type=argparse.FileType('w', encoding='UTF-8'),
                        help="the file to write the processed version of the glossary to")
    args = parser.parse_args()

    tasks[args.task](args.source, args.output)

    args.source.close()
    args.output.close()


if __name__ == "__main__":
    main()

    