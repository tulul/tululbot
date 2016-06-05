from telebot import types

from tululbot.utils import TululBot, lookup_kamusslang, lookup_urbandictionary, lookup_slang


class TestTululBot:

    def test_user_property(self, mocker, fake_user):
        bot = TululBot('TOKEN')
        mock_get_me = mocker.patch.object(bot, 'get_me', autospec=True,
                                          return_value=fake_user)

        rv = bot.user

        assert rv == fake_user
        mock_get_me.assert_called_once_with()

    def test_create_is_reply_to_filter(self, mocker, fake_message_dict, fake_user_dict):
        fake_replied_message_dict = fake_message_dict.copy()

        fake_message = types.Message.de_json(fake_message_dict)
        fake_replied_message = types.Message.de_json(fake_replied_message_dict)

        bot_user = types.User.de_json(fake_user_dict)
        bot_message = 'Message text from bot goes here'
        fake_replied_message.text = bot_message
        fake_replied_message.from_user = bot_user
        fake_message.reply_to_message = fake_replied_message

        bot = TululBot('TOKEN')
        bot.user = bot_user

        assert bot.create_is_reply_to_filter(bot_message)(fake_message)
        assert not bot.create_is_reply_to_filter('foo bar')(fake_message)


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

    mocker.patch('tululbot.utils.requests.get', autospec=True)
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup(), autospec=True)

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

    mocker.patch('tululbot.utils.requests.get', autospec=True)
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup(), autospec=True)

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

    mocker.patch('tululbot.utils.requests.get', autospec=True)
    mocker.patch('tululbot.utils.BeautifulSoup', return_value=FakeSoup(), autospec=True)

    rv = lookup_kamusslang('jdflafj')

    assert rv is None


def test_lookup_kamusslang_conn_error(mocker):
    class FakeResponse:
        def __init__(self):
            self.ok = False

    mocker.patch('tululbot.utils.requests.get', return_value=FakeResponse(), autospec=True)

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
    mocker.patch('tululbot.utils.ud.define', return_value=fake_definition, autospec=True)

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
    mocker.patch('tululbot.utils.ud.define', return_value=fake_no_definition, autospec=True)

    rv = lookup_urbandictionary('eemmbeekk')

    assert rv is None


def test_lookup_slang_when_only_urbandictionary_has_definition(mocker):
    fake_definition = 'soba ni itai yo'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=fake_definition,
                 autospec=True)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=None, autospec=True)

    rv = lookup_slang('kimi no tame ni dekiru koto ga, boku ni aru kana?')

    assert rv == fake_definition


def test_lookup_slang_when_only_kamusslang_has_definition(mocker):
    fake_definition = 'nagareru kisetsu no mannaka de'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=None, autospec=True)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=fake_definition,
                 autospec=True)

    rv = lookup_slang('futohi no nagasa wo kanjimasu')

    assert rv == fake_definition


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_no_definition(mocker):
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=None, autospec=True)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=None, autospec=True)

    rv = lookup_slang('hitomi wo tojireba anata ga')

    assert rv == 'Gak nemu cuy'


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_definition(mocker):
    fake_urbandict_def = 'mabuta no ura ni iru koto de'
    fake_kamusslang_def = 'dore hodo tsuyoku nareta deshou'
    mocker.patch('tululbot.utils.lookup_urbandictionary', return_value=fake_urbandict_def,
                 autospec=True)
    mocker.patch('tululbot.utils.lookup_kamusslang', return_value=fake_kamusslang_def,
                 autospec=True)

    rv = lookup_slang('anata ni totte watashi mo')

    fake_definition = (
        '\U000026AB *urbandictionary*:\n{}'
        '\n\n'
        '\U000026AB *kamusslang*:\n{}'
    ).format(fake_urbandict_def, fake_kamusslang_def)

    assert rv == fake_definition
