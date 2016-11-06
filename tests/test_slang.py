from tululbot.utils.slang import lookup_kamusslang, lookup_urbandictionary, lookup_slang


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

    mocker.patch('tululbot.utils.slang.requests.get', autospec=True)
    mocker.patch('tululbot.utils.slang.BeautifulSoup', return_value=FakeSoup(), autospec=True)

    rv = lookup_kamusslang('jdflafj')

    assert rv == 'Temporarily disabled.'


def test_lookup_kamusslang_no_definition_found(mocker):
    side_effect_pair = {
        'close-word-suggestion-text': None,
        'term-def': None
    }

    class FakeSoup:
        def find(self, class_):
            return side_effect_pair[class_]

    mocker.patch('tululbot.utils.slang.requests.get', autospec=True)
    mocker.patch('tululbot.utils.slang.BeautifulSoup', return_value=FakeSoup(), autospec=True)

    rv = lookup_kamusslang('jdflafj')

    assert rv == 'Temporarily disabled.'


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

    mocker.patch('tululbot.utils.slang.requests.get', autospec=True)
    mocker.patch('tululbot.utils.slang.BeautifulSoup', return_value=FakeSoup(), autospec=True)

    rv = lookup_kamusslang('jdflafj')

    assert rv == 'Temporarily disabled.'


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
    mocker.patch('tululbot.utils.slang.ud.define', return_value=fake_definition, autospec=True)

    rv = lookup_urbandictionary('eemmbeekk')

    assert rv == 'Temporarily disabled.'


def test_lookup_urbandictionary_no_definition_found(mocker):
    fake_no_definition = [
        {
            'def': "\nThere aren't any definitions for kimcil yet.\nCan you define it?\n",
            'example': '',
            'word': '¯\\_(ツ)_/¯\n'
            }
    ]
    mocker.patch('tululbot.utils.slang.ud.define', return_value=fake_no_definition,
                 autospec=True)

    rv = lookup_urbandictionary('eemmbeekk')

    assert rv == 'Temporarily disabled.'


def test_lookup_slang_when_only_urbandictionary_has_definition(mocker):
    fake_definition = 'soba ni itai yo'
    mocker.patch('tululbot.utils.slang.lookup_urbandictionary', return_value=fake_definition,
                 autospec=True)
    mocker.patch('tululbot.utils.slang.lookup_kamusslang', return_value=None, autospec=True)

    rv = lookup_slang('kimi no tame ni dekiru koto ga, boku ni aru kana?')

    assert rv == 'Temporarily disabled.'


def test_lookup_slang_when_only_kamusslang_has_definition(mocker):
    fake_definition = 'nagareru kisetsu no mannaka de'
    mocker.patch('tululbot.utils.slang.lookup_urbandictionary', return_value=None,
                 autospec=True)
    mocker.patch('tululbot.utils.slang.lookup_kamusslang', return_value=fake_definition,
                 autospec=True)

    rv = lookup_slang('futohi no nagasa wo kanjimasu')

    assert rv == 'Temporarily disabled.'


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_no_definition(mocker):
    mocker.patch('tululbot.utils.slang.lookup_urbandictionary', return_value=None,
                 autospec=True)
    mocker.patch('tululbot.utils.slang.lookup_kamusslang', return_value=None, autospec=True)

    rv = lookup_slang('hitomi wo tojireba anata ga')

    assert rv == 'Temporarily disabled.'


def test_lookup_slang_when_both_urbandictionary_and_kamusslang_have_definition(mocker):
    fake_urbandict_def = 'mabuta no ura ni iru koto de'
    fake_kamusslang_def = 'dore hodo tsuyoku nareta deshou'
    mocker.patch('tululbot.utils.slang.lookup_urbandictionary',
                 return_value=fake_urbandict_def, autospec=True)
    mocker.patch('tululbot.utils.slang.lookup_kamusslang', return_value=fake_kamusslang_def,
                 autospec=True)

    rv = lookup_slang('anata ni totte watashi mo')

    fake_definition = (
        '\U000026AB *urbandictionary*:\n{}'
        '\n\n'
        '\U000026AB *kamusslang*:\n{}'
    ).format(fake_urbandict_def, fake_kamusslang_def)

    assert rv == 'Temporarily disabled.'
