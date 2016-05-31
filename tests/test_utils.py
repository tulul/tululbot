import pytest
from telebot import types

from tululbot.utils import TululBot, lookup_kamusslang, lookup_urbandictionary, lookup_slang
from tululbot.types import Message


class TestTululBot:

    def test_create_bot(self):
        bot = TululBot('TOKEN')

        assert bot._telebot is not None
        assert bot._user is None

    def test_get_me(self, mocker):
        bot = TululBot('TOKEN')
        return_value = 'askldfjlkf'
        mock_get_me = mocker.patch.object(bot._telebot, 'get_me', autospec=True,
                                          return_value=return_value)

        rv = bot.get_me()

        assert rv == return_value
        mock_get_me.assert_called_once_with()

    def test_send_message(self, mocker):
        bot = TululBot('TOKEN')
        return_value = 'some return value'
        mock_send_message = mocker.patch.object(bot._telebot, 'send_message',
                                                return_value=return_value,
                                                autospec=True)
        chat_id = 12345
        text = 'Hello world'

        rv = bot.send_message(chat_id, text)

        assert rv == return_value
        mock_send_message.assert_called_once_with(chat_id, text)

    def test_set_webhook(self, mocker):
        bot = TululBot('TOKEN')
        return_value = 'some return value'
        webhook_url = 'some url'
        mock_set_webhook = mocker.patch.object(bot._telebot, 'set_webhook',
                                               return_value=return_value, autospec=True)

        rv = bot.set_webhook(webhook_url)

        assert rv == return_value
        mock_set_webhook.assert_called_once_with(webhook_url)

    def test_reply_to(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        return_value = 'some return value'
        mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to',
                                            return_value=return_value,
                                            autospec=True)
        text = 'Hello world'

        rv = bot.reply_to(fake_message, text)

        assert rv == return_value
        mock_reply_to.assert_called_once_with(fake_message, text,
                                              disable_web_page_preview=False,
                                              reply_markup=None)

    def test_reply_to_with_preview_disabled(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to', autospec=True)
        text = 'Hello world'

        bot.reply_to(fake_message, text, disable_preview=True)

        mock_reply_to.assert_called_once_with(fake_message, text,
                                              disable_web_page_preview=True,
                                              reply_markup=None)

    def test_reply_to_with_force_reply(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to', autospec=True)
        text = 'dummy text'

        bot.reply_to(fake_message, text, force_reply=True)

        args, kwargs = mock_reply_to.call_args
        assert args == (fake_message, text)
        assert len(kwargs) == 2
        assert 'disable_web_page_preview' in kwargs
        assert not kwargs['disable_web_page_preview']
        assert 'reply_markup' in kwargs
        assert isinstance(kwargs['reply_markup'], types.ForceReply)

    def test_forward_message(self, mocker):
        bot = TululBot('TOKEN')
        return_value = 'some return value'
        mock_forward_message = mocker.patch.object(bot._telebot, 'forward_message',
                                                   return_value=return_value,
                                                   autospec=True)
        chat_id = 12345
        from_chat_id = 67890
        message_id = 42

        rv = bot.forward_message(chat_id, from_chat_id, message_id)

        assert rv == return_value
        mock_forward_message.assert_called_once_with(chat_id, from_chat_id, message_id)

    def test_message_handler_with_no_argument(self):
        bot = TululBot('TOKEN')
        with pytest.raises(ValueError):
            @bot.message_handler()
            def handle(message):
                pass

    def test_equals_message_handler(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                                   autospec=True)

        @bot.message_handler(equals='/hello')
        def handle(message):
            pass

        args, kwargs = mock_message_handler.call_args
        assert len(args) == 0
        assert len(kwargs) == 1
        assert 'func' in kwargs
        func = kwargs['func']
        fake_message.text = '/hello'
        assert func(fake_message)
        fake_message.text = '/hello world'
        assert not func(fake_message)

    def test_is_reply_to_bot_message_handler(self, mocker, fake_message_dict, fake_user_dict):
        fake_reply_message_dict = fake_message_dict.copy()

        bot = TululBot('TOKEN')
        bot_id = 12345

        class FakeUser:
            def __init__(self, id):
                self.id = id

        bot.user = FakeUser(bot_id)
        mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                                   autospec=True)

        fake_user_dict['id'] = bot_id
        bot_message = 'Hah?'
        fake_message_dict['text'] = bot_message
        fake_message_dict['from'] = fake_user_dict
        fake_reply_message_dict['reply_to_message'] = fake_message_dict
        fake_reply_message = Message.from_dict(fake_reply_message_dict)

        @bot.message_handler(is_reply_to_bot=bot_message)
        def handle(message):
            pass

        args, kwargs = mock_message_handler.call_args
        assert len(args) == 0
        assert len(kwargs) == 1
        assert 'func' in kwargs
        func = kwargs['func']
        assert func(fake_reply_message)

    def test_commands_message_handler(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                                   autospec=True)

        @bot.message_handler(commands=['hello', 'world'])
        def handle(message):
            pass

        args, kwargs = mock_message_handler.call_args
        assert len(args) == 0
        assert len(kwargs) == 1
        assert 'func' in kwargs
        func = kwargs['func']
        fake_message.text = '/hello foo'
        assert func(fake_message)
        fake_message.text = '/world'
        assert func(fake_message)
        fake_message.text = '/brrrmm'
        assert not func(fake_message)

    def test_handle_new_message(self, mocker, fake_message):
        bot = TululBot('TOKEN')
        mock_process_new_messages = mocker.patch.object(bot._telebot, 'process_new_messages',
                                                        autospec=True)

        bot.handle_new_message(fake_message)

        mock_process_new_messages.assert_called_once_with([fake_message])

    def test_user_property(self, mocker, fake_user):
        bot = TululBot('TOKEN')
        mock_get_me = mocker.patch.object(bot, 'get_me', autospec=True,
                                          return_value=fake_user)

        rv = bot.user

        assert rv == fake_user
        mock_get_me.assert_called_once_with()


def test_lookup_kamusslang(mocker):
    class FakeParagraph:
        def __init__(self, strings):
            self.strings = strings

    strings = ['asdf', 'alsjdf', 'kfdg']

    side_effect_pair = {
        'close-word-suggestion-text': None,
        'term-def': FakeParagraph(strings)
    }

    class FakeSoup:
        def find(self, class_):
            return side_effect_pair[class_]

    mocker.patch('tululbot.utils.requests.get')
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup())

    rv = lookup_kamusslang('jdflafj')

    assert rv == ''.join(strings)


def test_lookup_kamusslang_no_definition_found(mocker):
    side_effect_pair = {
        'close-word-suggestion-text': None,
        'term-def': None
    }

    class FakeSoup:
        def find(self, class_):
            return side_effect_pair[class_]

    mocker.patch('tululbot.utils.requests.get')
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup())

    rv = lookup_kamusslang('jdflafj')

    assert rv is None


def test_lookup_kamusslang_close_word_suggestion(mocker):
    class FakeParagraph:
        def __init__(self, strings):
            self.strings = strings

    strings = ['asdf', 'alsjdf', 'kfdg']
    side_effect_pair = {
        'close-word-suggestion-text': 'Apalah',
        'term-def': FakeParagraph(strings)
    }

    class FakeSoup:
        def find(self, class_):
            return side_effect_pair[class_]

    mocker.patch('tululbot.utils.requests.get')
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup())

    rv = lookup_kamusslang('jdflafj')

    assert rv is None


def test_lookup_kamusslang_conn_error(mocker):
    class FakeResponse:
        def __init__(self):
            self.ok = False

    mocker.patch('tululbot.utils.requests.get', return_value=FakeResponse())

    rv = lookup_kamusslang('asdf jku')

    assert rv == "Koneksi lagi bapuk nih :'("


def test_lookup_urbandictionary(mocker):
    fake_definition = [
        {
            'def': 'mmeeeeooowww',
            'example': 'guk guk guk',
            'word': 'kaing kaing'
        },
        {
            'def': 'grrrrrrrr',
            'example': 'tokkeeeeekk tokkeeeekk',
            'word': 'aaauuuuuuuu'
        }
    ]
    mocker.patch('tululbot.utils.ud.define', return_value=fake_definition)

    rv = lookup_urbandictionary('eemmbeekk')

    assert rv == fake_definition[0]['def']


def test_lookup_urbandictionary_no_definition_found(mocker):
    fake_no_definition = [
        {
            'def': "\nThere aren't any definitions for kimcil yet.\nCan you define it?\n",
            'example': '',
            'word': '¯\\_(ツ)_/¯\n'
            }
    ]
    mocker.patch('tululbot.utils.ud.define', return_value=fake_no_definition)

    rv = lookup_urbandictionary('eemmbeekk')

    assert rv is None


def test_lookup_slang_when_only_urbandictionary_has_definition(mocker):
    fake_definition = 'soba ni itai yo'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=fake_definition)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=None)

    rv = lookup_slang('kimi no tame ni dekiru koto ga, boku ni aru kana?')

    assert rv == fake_definition


def test_lookup_slang_when_only_kamusslang_has_definition(mocker):
    fake_definition = 'nagareru kisetsu no mannaka de'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=None)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=fake_definition)

    rv = lookup_slang('futohi no nagasa wo kanjimasu')

    assert rv == fake_definition


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_no_definition(mocker):
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=None)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=None)

    rv = lookup_slang('hitomi wo tojireba anata ga')

    assert rv == 'Gak nemu cuy'


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_definition(mocker):
    fake_urbandict_def = 'mabuta no ura ni iru koto de'
    fake_kamusslang_def = 'dore hodo tsuyoku nareta deshou'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=fake_urbandict_def)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=fake_kamusslang_def)

    rv = lookup_slang('anata ni totte watashi mo')

    fake_definition = (
        '\U000126AB *urbandictionary*:\n{}'
        '\n\n'
        '\U000126AB *kamusslang*:\n{}'
    ).format(fake_urbandict_def, fake_kamusslang_def)

    assert rv == fake_definition
