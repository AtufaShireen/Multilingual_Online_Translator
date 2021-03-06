import requests
import argparse
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.your_language = ''
        self.word = ''
        self.file = None

    def input_data(self, lang_from, word):
        self.your_language = lang_from
        self.word = word
        self.file = open(self.word + '.txt', 'w', encoding='utf-8')

    def print(self, translate_to_next):
        url = 'https://context.reverso.net/translation/'
        url += self.your_language + '-' + translate_to_next + '/'
        url += self.word
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers)
        except Exception:
            print('Something wrong with your internet connection')
            exit()
        if r.status_code != 200:
            print(f'Sorry, unable to find {self.word}')
            exit()
        soup = BeautifulSoup(r.content, 'html.parser')
        self.file.write('\n')
        print()
        translations = '' + translate_to_next.title() + ' Translations:'
        print(translations)
        self.file.write(translations + '\n')
        a = soup.find_all('a', class_='translation')
        for i1 in a:
            one_word = i1.text.strip()
            print(one_word)
            self.file.write(str(one_word) + '\n')
        print()
        self.file.write('\n')
        examples = "" + translate_to_next.title() + ' Examples:'
        print(examples)
        self.file.write(examples + '\n')
        div = soup.find_all('div', {'class': 'example'})
        for i2 in div:
            example_from = i2.contents[1].text.strip()
            print(example_from)
            self.file.write(str(example_from) + '\n')
            example_to = i2.contents[3].text.strip()
            print(example_to)
            self.file.write(str(example_to) + '\n')
            self.file.write('\n')
            print()


languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
             'romanian', 'russian', 'turkish']
parser = argparse.ArgumentParser()
parser.add_argument("lang_from")
parser.add_argument("lang_to")
parser.add_argument("word")
args = parser.parse_args()
translator = Translator()
translator.input_data(args.lang_from, args.word)

if args.lang_to == 'all':
    for i in languages:
        translator.print(i)
elif args.lang_to not in languages:
    print(f"Sorry, the program doesn't support {args.lang_to}")
    exit()
else:
    translator.print(args.lang_to)

translator.file.close()
