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

tasks = {
    'alpha': 'alphabetise',
    'syn': 'synonyms',
}

def synonyms(source: io.TextIOWrapper, output: io.TextIOWrapper):
    json_list = list(source)
    entry_list = list(map(json.loads, json_list))
    meanings_tracker = {}
    for entry in entry_list:
        try:
            entry['synonymOf'] = meanings_tracker[str(entry['meanings'])]['origin']
            entry.pop('meanings', None)
        except KeyError:
            meanings_tracker[str(entry['meanings'])] = {
                'origin': entry['plaintext'],
                'count': 0, 
            }
    output.writelines("\n".join(
        map(lambda x: json.dumps(x, ensure_ascii=False), entry_list)))
 

def alphabetise(source: io.TextIOWrapper, output: io.TextIOWrapper):
    json_list = list(source)
    entry_list = list(map(json.loads, json_list))
    entry_list.sort(key=lambda entry : entry['plaintext'])
    output.writelines("\n".join(
        map(lambda x: json.dumps(x, ensure_ascii=False), entry_list)))


def main():
    parser = argparse.ArgumentParser(description='Process a JSON-lines glossary file.')
    parser.add_argument("task", choices=tasks.values())
    parser.add_argument("source", type=argparse.FileType('r', encoding='UTF-8'), 
                        help="the current glossary file")
    parser.add_argument("output", type=argparse.FileType('w', encoding='UTF-8'),
                        help="the file to write the processed version of the glossary to")
    args = parser.parse_args()

    if args.task == tasks['alpha']:
        alphabetise(args.source, args.output)
    elif args.task == tasks['syn']:
        synonyms(args.source, args.output)
    else:
        parser.print_help()

    args.source.close()
    args.output.close()


if __name__ == "__main__":
    main()

    