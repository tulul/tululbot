import random
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import requests
from telebot import TeleBot, types
import urbandict as ud
import yaml


class TululBot(TeleBot):

    def __init__(self, token):
        super(TululBot, self).__init__(token)
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

    def reply_to(self, *args, **kwargs):
        try:
            force_reply = kwargs.pop('force_reply')
        except KeyError:
            return super(TululBot, self).reply_to(*args, **kwargs)
        else:
            if force_reply:
                kwargs['reply_markup'] = types.ForceReply(selective=True)
            return super(TululBot, self).reply_to(*args, **kwargs)

    def create_is_reply_to_filter(self, text):
        def is_reply_to_bot(message):
            return (self.is_reply_to_bot_user(message) and
                    message.reply_to_message.text == text)

        return is_reply_to_bot

    def is_reply_to_bot_user(self, message):
        replied_message = message.reply_to_message
        return (replied_message is not None and
                replied_message.from_user is not None and
                replied_message.from_user.id == self.user.id)


class QuoteEngine:

    def __init__(self):
        self.quote_url = 'https://raw.githubusercontent.com/tulul/tulul-quotes/master/quote.yaml'  # noqa
        # Note: rawgit does not have 100% uptime, but at
        # least they're not throttling us.

        self.cache = []

    def retrieve_random(self):
        if not self.cache:
            self.refresh_cache()

        return self.format_quote(random.choice(self.cache))

    def format_quote(self, q):
        return '{q[quote]} - {q[author]}, {q[author_bio]}'.format(q=q)

    def refresh_cache(self):
        body = requests.get(self.quote_url).text
        # What if previosuly we have the cache, but this time
        # when we try to get new cache, the network occurs error?
        # We will think about "don't refresh if error" later.
        self.cache = yaml.load(body)['quotes']


def lookup_slang(word):
    not_found_word = 'Gak nemu cuy'
    return lookup_slang_sources(word) or not_found_word


def lookup_slang_sources(word):
    urbandict_def = lookup_urbandictionary(word)
    kamusslang_def = lookup_kamusslang(word)
    if urbandict_def is not None and kamusslang_def is not None:
        return (
            '\U000026AB *urbandictionary*:\n{}'
            '\n\n'
            '\U000026AB *kamusslang*:\n{}'
        ).format(urbandict_def.strip(), kamusslang_def.strip())
    return urbandict_def or kamusslang_def


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

    if urbandictionary_has_definition(res[0]):
        return res[0]['def']

    return None


def urbandictionary_has_definition(definition):
    return "There aren't any definition" not in definition['def']
