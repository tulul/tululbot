import random

import requests
from telebot import TeleBot, types
import yaml


class TululBot:

    def __init__(self, token):
        self._telebot = TeleBot(token)
        self.user = None

    def get_me(self):
        self.user = self._telebot.get_me()

    def send_message(self, chat_id, text):
        return self._telebot.send_message(chat_id, text)

    def reply_to(self, message, text, disable_preview=False, force_reply=False):
        reply_markup = types.ForceReply(selective=True) if force_reply else None

        return self._telebot.reply_to(message, text,
                                      disable_web_page_preview=disable_preview,
                                      reply_markup=reply_markup)

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

    def _initialize_bot_user(self):
        if self.user is None:
            self.get_me()

    def _is_reply_to_bot_user(self, message):
        self._initialize_bot_user()
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
