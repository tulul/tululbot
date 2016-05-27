import re
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

from . import app, bot
from .utils import QuoteEngine, lookup_slang


quote_engine = QuoteEngine()
HOTLINE_MESSAGE_ID = app.config['HOTLINE_MESSAGE_ID']


@bot.message_handler(is_reply_to_bot='Apa yang mau dileli?')
@bot.message_handler(commands=['leli'])
def leli(message):
    app.logger.debug('Detected as leli command')
    term = _extract_leli_term(message)
    if not term:
        return bot.reply_to(message, 'Apa yang mau dileli?',
                            force_reply=True)
    else:
        result = _search_on_wikipedia(term)
        if result is None:
            result = _search_on_google(term)
        return bot.reply_to(message, result, disable_preview=True)


@bot.message_handler(commands=['quote'])
def quote(message):
    app.logger.debug('Detected as quote command')
    return bot.reply_to(message, quote_engine.retrieve_random())


@bot.message_handler(commands=['who'])
def who(message):
    app.logger.debug('Detected as who command')
    about_text = (
        'TululBot v1.5.3\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    return bot.reply_to(message, about_text, disable_preview=True)


@bot.message_handler(is_reply_to_bot='Apa yang mau dicari jir?')
@bot.message_handler(commands=['slang'])
def slang(message):
    app.logger.debug('Detected as slang command')
    word = _extract_slang_word(message)

    if word is None:
        return bot.reply_to(message, 'Apa yang mau dicari jir?', force_reply=True)
    else:
        slang_definition = lookup_slang(word)
        return bot.reply_to(message, slang_definition)


@bot.message_handler(commands=['hotline'])
def hotline(message):
    app.logger.debug('Detected as hotline command')
    if HOTLINE_MESSAGE_ID is not None:
        return bot.forward_message(message.chat.id, message.chat.id, HOTLINE_MESSAGE_ID)


@bot.message_handler(is_reply_to_bot='Siapa yang ultah?')
@bot.message_handler(commands=['hbd'])
def hbd(message):
    app.logger.debug('Detected as hbd command')
    name = _extract_birthday_boy_or_girl_name(message)
    if not name:
        return bot.reply_to(message, 'Siapa yang ultah?',
                            force_reply=True)
    else:
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(name)
        return bot.send_message(message.chat.id, greetings)


def _extract_leli_term(message):
    assert message.text is not None
    return message.text[6:] if message.text.startswith('/leli') else message.text


def _extract_slang_word(message):
    return _extract_word(message, "slang")


def _extract_birthday_boy_or_girl_name(message):
    return _extract_word(message, "hbd")


def _extract_word(message, command_name):
    assert message.text is not None

    if message.text.startswith("/{}".format(command_name)):
        regexp = r'/{}(@{})? (?P<word>.+)$'.format(command_name, bot.user.first_name)
        match = re.match(regexp, message.text)
        return match.groupdict()['word'] if match is not None else None
    else:
        return message.text


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
    return BeautifulSoup(page, 'html.parser').find('div', id='mw-content-text')


def _search_on_google(term):
    query_string = urlencode(dict(q=term))
    search_url = 'https://google.com/search?{}'.format(query_string)
    return 'Jangan ngeleli! Googling dong: {}'.format(search_url)
