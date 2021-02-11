#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import requests
import argparse
from language import language
#from dictionary.language import language

import anki


def get_parser():
    parser = argparse.ArgumentParser(
        prog='cli-dictionary', description='welcome to cli-dictionary, never use a browser again to get a word meaning ;)')
    parser.add_argument('word', type=str, help='the word to be searched.')
    parser.add_argument(
        'lang', type=str, help='the language of the requested word.')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 2.3.1')
    parser.add_argument('-s', '--synonyms', action='store_true',
                        help='display the synonyms of the requested word.')
    parser.add_argument('-e', '--examples', action='store_true',
                        help='display a phrase using the requested word.')

    group_anki = parser.add_argument_group('Anki-Flashcards')
    group_anki.add_argument(
        '--card', help='select the type of card', choices=['basic', 'basic-reverse'])
    group_anki.add_argument(
        '--profile', help='select the profile', type=str, nargs=1)

    return parser


def main(word, lang, *args):
    word = word.encode('utf-8')

    sy = ''  # synonyms
    ex = ''  # examples
    global Anki

    for arg in args:
        sy = arg[0]['synonyms']
        ex = arg[0]['examples']
        Anki = arg[0]['card'] if arg[0]['profile'] == None else arg[0]['profile']

    # upper() because in list of language.py all the abbreviation are uppercased.
    lang = lang.upper()

    if lang in language:
        url = language[lang] + word.decode('utf-8')
        meaning(url, synonyms=sy, examples=ex)
    else:
        print("""
           select a valid language:
           en <english> | pt <portuguese>
           hi <hindi>   | es <spanish>
           fr <french>  | ja <japanese>
           ru <russian> | de <german>
           it <italian> | ko <korean>
           zh <chinese> | ar <arabic>
           tr <turkish>
       """)


def meaning(url, **kwargs):
    header = {
        "Accept": "charset=utf-8"
    }

    response = requests.request('GET', url, headers=header)

    data = json.loads(response.text.encode('utf-8'))

    for obj in data:

        meanings = obj['meanings'][0]['definitions']

        # always show the definition - default
        get_data('DEFINITIONS', meanings, 'definition')

        if kwargs.get('examples'):
            get_data('EXAMPLES', meanings, 'example')

        if kwargs.get('synonyms'):
            # get index of the synonym
            get_data('SYNONYMS', meanings, 'synonyms', j=0)


def get_data(title, array, key, **kwargs):
    try:
        i = 0
        print(title + ' ----------------------')

        j = kwargs.get('j')

        if j != 0:
            for element in array:
                i = i + 1
                print(f'{str(i)}. {element[key]}')
        else:
            for element in array:
                i = i + 1
                j = j + 1
                print(f'{str(i)}. {element[key][j]}')

    except (IndexError, TypeError):
        print('sorry, we could not find the word you are looking for :(')
        return

    except KeyError:
        return


if __name__ == '__main__':
    parser = get_parser()
    args = vars(parser.parse_args())
    main(sys.argv[1], sys.argv[2], [args])
