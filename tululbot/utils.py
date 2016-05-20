import random
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import requests
from telebot import TeleBot, types
import urbandict as ud
import yaml


class TululBot:

    def __init__(self, token):
        self._telebot = TeleBot(token)
        self._user = None

    @property
    def user(self):
        if self._user is not None:
            return self._user

        self._user = self.get_me()
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def get_me(self):
        return self._telebot.get_me()

    def send_message(self, chat_id, text):
        return self._telebot.send_message(chat_id, text)

    def set_webhook(self, webhook_url):
        return self._telebot.set_webhook(webhook_url)

    def reply_to(self, message, text, disable_preview=False, force_reply=False):
        reply_markup = types.ForceReply(selective=True) if force_reply else None

        return self._telebot.reply_to(message, text,
                                      disable_web_page_preview=disable_preview,
                                      reply_markup=reply_markup)

    def forward_message(self, chat_id, from_chat_id, message_id):
        return self._telebot.forward_message(chat_id, from_chat_id, message_id)

    def message_handler(self, equals=None, is_reply_to_bot=None, commands=None):
        if equals is not None:
            kwargs = {'func': self._make_equals_func(equals)}
        elif is_reply_to_bot is not None:
            kwargs = {'func': self._make_is_reply_to_bot_func(is_reply_to_bot)}
        elif commands is not None:
            kwargs = {'commands': commands}
        else:
            raise ValueError('Argument must be given')

        return self._telebot.message_handler(**kwargs)

    def handle_new_message(self, message):
        self._telebot.process_new_messages([message])

    @staticmethod
    def _make_equals_func(text):
        def equals(message):
            message_text = TululBot._get_text(message)
            return message_text is not None and message_text == text
        return equals

    @staticmethod
    def _get_text(message):
        try:
            return message.text
        except AttributeError:
            return None

    def _make_is_reply_to_bot_func(self, text):
        def is_reply_to_bot(message):
            if not self._is_reply_to_bot_user(message):
                return False
            else:
                message_text = self._get_text(message.reply_to_message)
                return message_text == text

        return is_reply_to_bot

    def _is_reply_to_bot_user(self, message):
        replied_message = message.reply_to_message
        return (replied_message is not None and
                replied_message.from_user is not None and
                replied_message.from_user.id == self.user.id)


class QuoteEngine:

    def __init__(self):
        self._quote_url = 'https://raw.githubusercontent.com/tulul/tulul-quotes/master/quote.yaml'  # noqa
        # Note: rawgit does not have 100% uptime, but at
        # least they're not throttling us.

        self._cache = []

    def retrieve_random(self):
        if not self._cache:
            self.refresh_cache()

        cache = self._cache
        return self.format_quote(random.choice(cache))

    def format_quote(self, q):
        return '{q[quote]} - {q[author]}, {q[author_bio]}'.format(q=q)

    def refresh_cache(self):
        body = requests.get(self._quote_url).text
        # What if previosuly we have the cache, but this time
        # when we try to get new cache, the network occurs error?
        # We will think about "don't refresh if error" later.
        self._cache = yaml.load(body)['quotes']


def lookup_slang(word):
    not_found_word = 'Gak nemu cuy'
    return lookup_slang_sources(word) or not_found_word


def lookup_slang_sources(word):
    urbandic_def = lookup_urbandictionary(word)
    kamusslang_def = lookup_kamusslang(word)
    if urbandic_def is not None and kamusslang_def is not None:
        return (
            'urbandictionary:\n{}'
            '\n\n'
            'kamusslang:\n{}'
        ).format(urbandic_def, kamusslang_def)
    else:
        return urbandic_def or kamusslang_def


def lookup_kamusslang(word):
    """Lookup slang word definition on kamusslang.com.

    Returns None if no definition found.
    """
    kamusslang_url_format = 'http://kamusslang.com/arti/{}'
    url = kamusslang_url_format.format(quote_plus(word))
    r = requests.get(url)

    if not r.ok:
        return "Koneksi lagi bapuk nih :'("

    doc = BeautifulSoup(r.text, 'html.parser')
    paragraph = doc.find(class_='term-def')

    # Prevent word-alike suggestion
    if doc.find(class_='close-word-suggestion-text') is not None:
        return None

    return ''.join(paragraph.strings) if paragraph is not None else None


def lookup_urbandictionary(word):
    """Lookup word definition on urbandictionary.com.

    Returns None if no definition found.
    """
    res = ud.define(word)
    assert res  # res is never empty, even when no definition is found

    if _urbandictionary_has_definition(res[0]):
        return res[0]['def']

    return None


def _urbandictionary_has_definition(definition):
    return "There aren't any definition" not in definition['def']
