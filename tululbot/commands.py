from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

from . import app, bot
from .utils import QuoteEngine, lookup_slang


quote_engine = QuoteEngine()
HOTLINE_MESSAGE_ID = app.config['HOTLINE_MESSAGE_ID']
BOT_USERNAME = app.config['TELEGRAM_BOT_USERNAME']


@bot.message_handler(func=bot.create_is_reply_to_filter('Apa yang mau dileli?'))
@bot.message_handler(regexp=r'^/leli(@{})?( .+)*$'.format(BOT_USERNAME))
def leli(message):
    app.logger.debug('Detected leli command {!r}'.format(message.text))
    try:
        if message.text.startswith('/leli'):
            _, term = message.text.split(' ', maxsplit=1)
        else:
            term = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Apa yang mau dileli?', force_reply=True)
    else:
        app.logger.debug('Extracted leli term {!r}'.format(term))
        result = search_on_wikipedia(term)
        if result is None:
            result = search_on_google(term)
        bot.reply_to(message, result, disable_web_page_preview=True)


@bot.message_handler(regexp=r'^/quote(@{})?$'.format(BOT_USERNAME))
def quote(message):
    app.logger.debug('Detected quote command {!r}'.format(message.text))
    return bot.reply_to(message, quote_engine.retrieve_random())


@bot.message_handler(regexp=r'^/who(@{})?$'.format(BOT_USERNAME))
def who(message):
    app.logger.debug('Detected who command {!r}'.format(message.text))
    about_text = (
        'TululBot v1.7.4\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    return bot.reply_to(message, about_text, disable_web_page_preview=True)


@bot.message_handler(func=bot.create_is_reply_to_filter('Apa yang mau dicari jir?'))
@bot.message_handler(regexp=r'^/slang(@{})?( \w+)*$'.format(BOT_USERNAME))
def slang(message):
    app.logger.debug('Detected slang command {!r}'.format(message.text))
    try:
        if message.text.startswith('/slang'):
            _, term = message.text.split(' ', maxsplit=1)
        else:
            term = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Apa yang mau dicari jir?', force_reply=True)
    else:
        app.logger.debug('Extracted slang term {!r}'.format(term))
        bot.reply_to(message, lookup_slang(term), parse_mode='Markdown')


@bot.message_handler(regexp=r'^/hotline(@{})?$'.format(BOT_USERNAME))
def hotline(message):
    app.logger.debug('Detected hotline command {!r}'.format(message.text))
    if HOTLINE_MESSAGE_ID is not None:
        bot.forward_message(message.chat.id, message.chat.id, HOTLINE_MESSAGE_ID)


@bot.message_handler(func=bot.create_is_reply_to_filter('Siapa yang ultah?'))
@bot.message_handler(regexp=r'^/hbd(@{})?( @?\w+)*$'.format(BOT_USERNAME))
def hbd(message):
    app.logger.debug('Detected hbd command {!r}'.format(message.text))
    try:
        if message.text.startswith('/hbd'):
            _, name = message.text.split(' ', maxsplit=1)
        else:
            name = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Siapa yang ultah?', force_reply=True)
    else:
        app.logger.debug('Extracted hbd name {!r}'.format(name))
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(name)
        bot.send_message(message.chat.id, greetings)


def search_on_wikipedia(term):
    search_url = 'https://en.wikipedia.org/w/index.php'

    response = requests.get(search_url, params=dict(search=term))
    if not response.ok:
        return None

    page = response.text
    if not has_result(page):
        return None

    first_paragraph = parse_first_paragraph(page)
    if not has_disambiguations(first_paragraph.get_text()):
        return first_paragraph.get_text()

    disambiguation_url = parse_first_disambiguation_link(page)

    response = requests.get(disambiguation_url)
    if not response.ok:
        return None

    disambiguated_page = response.text
    return parse_first_paragraph(disambiguated_page).get_text()


def parse_first_disambiguation_link(page):
    def valid_link(tag):
        return tag.name == 'a' and tag['href'].startswith('/wiki')

    path = parse_content_text(page).find(valid_link)['href']
    return 'https://en.wikipedia.org{}'.format(path)


def has_disambiguations(paragraph):
    return 'may refer to:' in paragraph


def has_result(page):
    return ('Search results' not in page and
            parse_first_paragraph(page) is not None)


def parse_first_paragraph(page):
    return parse_content_text(page).find('p')


def parse_content_text(page):
    return BeautifulSoup(page, 'html.parser').find('div', id='mw-content-text')


def search_on_google(term):
    query_string = urlencode(dict(q=term))
    search_url = 'https://google.com/search?{}'.format(query_string)
    return 'Jangan ngeleli! Googling dong: {}'.format(search_url)
