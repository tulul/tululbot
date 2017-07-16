from urllib.parse import quote_plus

from requests import HTTPError

from bs4 import BeautifulSoup
import requests
import urbandict as ud


def lookup_slang(word):
    not_found_word = 'Gak nemu cuy'
    return lookup_slang_sources(word) or not_found_word


def lookup_slang_sources(word):
    urbandict_def = lookup_urbandictionary(word)

    try:
        kamusslang_def = lookup_kamusslang(word)
    except HTTPError:
        kamusslang_def = None

    if urbandict_def is not None and kamusslang_def is not None:
        return (
            '\U000026AB *urbandictionary*:\n{}'
            '\n\n'
            '\U000026AB *kamusslang*:\n{}'
        ).format(urbandict_def.strip(), kamusslang_def.strip())
    return urbandict_def or kamusslang_def


def lookup_kamusslang(word):
    """Look up slang word definition on kamusslang.com.

    Returns None if no definition found.
    """
    kamusslang_url_format = 'http://kamusslang.com/arti/{}'
    url = kamusslang_url_format.format(quote_plus(word))
    r = requests.get(url)
    r.raise_for_status()

    doc = BeautifulSoup(r.text, 'html.parser')
    paragraph = doc.find(class_='term-def')

    # Prevent word-alike suggestion
    if doc.find(class_='close-word-suggestion-text') is not None:
        return None

    return ''.join(paragraph.strings) if paragraph is not None else None


def lookup_urbandictionary(word):
    """Look up word definition on urbandictionary.com.

    Returns None if no definition found.
    """
    res = ud.define(word)
    assert res  # res is never empty, even when no definition is found

    if urbandictionary_has_definition(res[0]):
        return res[0]['def']

    return None


def urbandictionary_has_definition(definition):
    return "There aren't any definition" not in definition['def']
