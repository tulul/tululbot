from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

from . import app, bot
from .utils import QuoteEngine


quote_engine = QuoteEngine()


@bot.message_handler(is_reply_to_bot='Apa yang mau dileli?')
@bot.message_handler(startswith='/leli ')
def leli(message):
    app.logger.debug('Detected as leli command')
    term = _extract_term(message)
    if not term:
        return bot.reply_to(message, 'Apa yang mau dileli?',
                            force_reply=True)
    else:
        result = _search_on_wikipedia(term)
        if result is None:
            result = _search_on_google(term)
        return bot.reply_to(message, result, disable_preview=True)


@bot.message_handler(equals='/quote')
def quote(message):
    app.logger.debug('Detected as quote command')
    return bot.reply_to(message, quote_engine.retrieve_random())


@bot.message_handler(equals='/who')
def who(message):
    app.logger.debug('Detected as who command')
    about_text = (
        'TululBot v1.0.0\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    return bot.reply_to(message, about_text, disable_preview=True)


def _extract_term(message):
    assert message.text is not None
    return message.text[6:] if message.text.startswith('/leli') else message.text


def _search_on_wikipedia(term):
    query_string = urlencode(dict(search=term))
    search_url = \
        'https://en.wikipedia.org/w/index.php?{}'.format(query_string)

    response = requests.get(search_url)
    if response.status_code != 200:
        return None

    page = response.text
    if not _has_result(page):
        return None

    first_paragraph = _parse_first_paragraph(page)
    if not _has_disambiguations(first_paragraph.get_text()):
        return first_paragraph.get_text()

    disambiguation_url = _parse_first_disambiguation_link(page)

    response = requests.get(disambiguation_url)
    if response.status_code != 200:
        return None

    disambiguated_page = response.text
    return _parse_first_paragraph(disambiguated_page).get_text()


def _parse_first_disambiguation_link(page):
    def valid_link(tag):
        return tag.name == 'a' and tag['href'].startswith('/wiki')

    path = _parse_content_text(page).find(valid_link)['href']
    return 'https://en.wikipedia.org{}'.format(path)


def _has_disambiguations(paragraph):
    return 'may refer to:' in paragraph


def _has_result(page):
    return ('Search results' not in page and
            _parse_first_paragraph(page) is not None)


def _parse_first_paragraph(page):
    return _parse_content_text(page).find('p')


def _parse_content_text(page):
    return BeautifulSoup(page).find('div', id='mw-content-text')


def _search_on_google(term):
    query_string = urlencode(dict(q=term))
    search_url = 'https://google.com/search?{}'.format(query_string)
    return 'Jangan ngeleli! Googling dong: {}'.format(search_url)
