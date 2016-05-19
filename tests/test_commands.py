from unittest.mock import call, MagicMock

from tululbot.commands import leli, quote, who, slang, hotline, hbd


class TestLeliCommand:

    def test_with_no_term(self, fake_message, mocker):
        fake_message.text = '/leli'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to',
                                     autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Apa yang mau dileli?',
                                              force_reply=True)

    def test_with_term_found_on_wikipedia(self, fake_message, mocker):
        fake_message.text = '/leli tulul'
        mock_requests = mocker.patch('tululbot.commands.requests', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = (
            '<html>'
            '    <div id="mw-content-text">'
            '        <p>Tulul is the synonym of cool.</p>'
            '    </div>'
            '</html>'
        )

        leli(fake_message)

        mock_requests.get.assert_called_once_with(
            'https://en.wikipedia.org/w/index.php?search=tulul'
        )
        mock_reply_to.assert_called_once_with(
            fake_message, 'Tulul is the synonym of cool.',
            disable_preview=True
        )

    def test_with_ambiguous_term_on_wikipedia(self, fake_message, mocker):
        fake_message.text = '/leli snowden'
        mock_requests = mocker.patch('tululbot.commands.requests', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        class FakeResponse:
            pass

        response1 = FakeResponse()
        response1.status_code = 200
        response1.text = (
            '<html>'
            '    <div id="mw-content-text">'
            '        <p>Snowden may refer to:</p>'
            '        <ul>'
            '            <li><a href="/wiki/link1">Snowden1</a></li>'
            '            <li><a href="/wiki/link2">Snowden2</a></li>'
            '        </ul>'
            '    </div>'
            '</html>'
        )
        response2 = FakeResponse()
        response2.status_code = 200
        response2.text = (
            '<html>'
            '    <div id="mw-content-text">'
            '        <p>Snowden is former CIA employee.</p>'
            '    </div>'
            '</html>'
        )

        mock_requests.get.side_effect = [response1, response2]

        leli(fake_message)

        assert mock_requests.get.call_args_list == [
            call('https://en.wikipedia.org/w/index.php?search=snowden'),
            call('https://en.wikipedia.org/wiki/link1')
        ]
        mock_reply_to.assert_called_once_with(
            fake_message, 'Snowden is former CIA employee.',
            disable_preview=True
        )

    def test_with_term_resorted_on_google(self, fake_message, mocker):
        fake_message.text = '/leli wazaundtechnik'
        mock_requests = mocker.patch('tululbot.commands.requests', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = (
            '<html>'
            '<h1>Search results</h1>'
            '</html>'
        )

        leli(fake_message)

        mock_requests.get.assert_called_once_with(
            'https://en.wikipedia.org/w/index.php?search=wazaundtechnik'
        )
        expected_text = (
            'Jangan ngeleli! Googling dong: '
            'https://google.com/search?q=wazaundtechnik'
        )
        mock_reply_to.assert_called_once_with(
            fake_message, expected_text, disable_preview=True
        )


def test_quote(fake_message, mocker):
    fake_message.text = '/quote'
    mock_engine = mocker.patch('tululbot.commands.quote_engine', autospec=True)
    mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)
    mock_engine.retrieve_random.return_value = 'some random quote'

    quote(fake_message)

    mock_reply_to.assert_called_once_with(fake_message, 'some random quote')


def test_who(fake_message, mocker):
    fake_message.text = '/who'
    mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

    who(fake_message)

    expected_text = (
        'TululBot v1.2.1\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    mock_reply_to.assert_called_once_with(
        fake_message, expected_text, disable_preview=True
    )


def test_slang(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.reply_to = MagicMock()

    fake_bot = FakeBot()
    slang_word = 'hohoi ahoi'
    fake_message.text = '/slang {}'.format(slang_word)
    slang_lookup_result = 'hahaha'
    mocker.patch('tululbot.commands.bot', new=fake_bot)
    mock_lookup_slang = mocker.patch('tululbot.commands.lookup_slang',
                                     return_value=slang_lookup_result)

    slang(fake_message)

    mock_lookup_slang.assert_called_once_with(slang_word)
    fake_bot.reply_to.assert_called_once_with(fake_message, slang_lookup_result)


def test_slang_with_bot_name(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.reply_to = MagicMock()

    fake_bot = FakeBot()
    slang_word = 'hohoi'
    fake_message.text = '/slang@{} {}'.format(fake_bot.user.first_name, slang_word)
    slang_lookup_result = 'hahaha'
    mocker.patch('tululbot.commands.bot', new=fake_bot)
    mock_lookup_slang = mocker.patch('tululbot.commands.lookup_slang',
                                     return_value=slang_lookup_result)

    slang(fake_message)

    mock_lookup_slang.assert_called_once_with(slang_word)
    fake_bot.reply_to.assert_called_once_with(fake_message, slang_lookup_result)


def test_slang_no_word(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.reply_to = MagicMock()

    fake_bot = FakeBot()
    fake_message.text = '/slang'
    mocker.patch('tululbot.commands.bot', new=fake_bot)

    slang(fake_message)

    fake_bot.reply_to.assert_called_once_with(fake_message, 'Apa yang mau dicari jir?',
                                              force_reply=True)


def test_hotline(fake_message, mocker):
    fake_message.text = '/hotline'
    mock_hotline_message_id = mocker.patch('tululbot.commands.HOTLINE_MESSAGE_ID')
    mock_forward_message = mocker.patch('tululbot.commands.bot.forward_message')

    hotline(fake_message)

    mock_forward_message.assert_called_once_with(
        fake_message.chat.id, fake_message.chat.id, mock_hotline_message_id
    )


def test_hbd(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.send_message = MagicMock()

    fake_bot = FakeBot()
    fake_name = "Tutu Lulul"
    fake_message.text = '/hbd {}'.format(fake_name)
    greetings_format = ('hoi {}'
                        ' met ultah ya moga sehat dan sukses selalu '
                        '\xF0\x9F\x8E\x89 \xF0\x9F\x8E\x8A')
    greetings = greetings_format.format(fake_name)

    mocker.patch('tululbot.commands.bot', new=fake_bot)
    mock_send_message = mocker.patch('tululbot.commands.bot.send_message')

    hbd(fake_message)

    mock_send_message.assert_called_once_with(fake_message.chat.id, greetings)


def test_hbd_with_bot_name(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.send_message = MagicMock()

    fake_bot = FakeBot()
    fake_name = "Tutu Lulul"
    fake_message.text = '/hbd@{} {}'.format(
        fake_bot.user.first_name,
        fake_name
    )
    greetings_format = ('hoi {}'
                        ' met ultah ya moga sehat dan sukses selalu '
                        '\xF0\x9F\x8E\x89 \xF0\x9F\x8E\x8A')
    greetings = greetings_format.format(fake_name)
    mocker.patch('tululbot.commands.bot', new=fake_bot)
    mock_send_message = mocker.patch('tululbot.commands.bot.send_message')

    hbd(fake_message)

    mock_send_message.assert_called_once_with(fake_message.chat.id, greetings)


def test_hbd_no_word(fake_message, fake_user, mocker):
    class FakeBot:
        def __init__(self):
            self.user = fake_user
            self.reply_to = MagicMock()

    fake_bot = FakeBot()
    fake_message.text = '/hbd'
    mocker.patch('tululbot.commands.bot', new=fake_bot)

    hbd(fake_message)

    fake_bot.reply_to.assert_called_once_with(fake_message, 'Siapa yang ultah?',
                                              force_reply=True)
