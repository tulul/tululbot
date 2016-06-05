from tululbot.commands import leli, quote, who, slang, hotline, hbd


class TestLeliCommand:

    def test_with_no_term(self, mocker, fake_message):
        fake_message.text = '/leli'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

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

        mock_reply_to.assert_called_once_with(fake_message, 'Tulul is the synonym of cool.',
                                              disable_web_page_preview=True)

    def test_with_ambiguous_term_on_wikipedia(self, fake_message, mocker):
        fake_message.text = '/leli snowden'
        mock_requests = mocker.patch('tululbot.commands.requests', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        class FakeResponse:
            pass

        response1 = FakeResponse()
        response1.ok = True
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
        response2.ok = True
        response2.text = (
            '<html>'
            '    <div id="mw-content-text">'
            '        <p>Snowden is former CIA employee.</p>'
            '    </div>'
            '</html>'
        )

        mock_requests.get.side_effect = [response1, response2]

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Snowden is former CIA employee.',
                                              disable_web_page_preview=True)

    def test_with_term_resorted_on_google(self, fake_message, mocker):
        fake_message.text = '/leli wazaundtechnik'
        mock_requests = mocker.patch('tululbot.commands.requests', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        mock_requests.get.return_value.ok = True
        mock_requests.get.return_value.text = (
            '<html>'
            '<h1>Search results</h1>'
            '</html>'
        )

        leli(fake_message)

        expected_text = (
            'Jangan ngeleli! Googling dong: '
            'https://google.com/search?q=wazaundtechnik'
        )
        mock_reply_to.assert_called_once_with(fake_message, expected_text,
                                              disable_web_page_preview=True)


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
        'TululBot v1.7.2\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    mock_reply_to.assert_called_once_with(fake_message, expected_text,
                                          disable_web_page_preview=True)


class TestSlangCommand:

    def test_slang(self, mocker, fake_message):
        slang_term = 'hohoi ahoi'
        fake_message.text = '/slang {}'.format(slang_term)
        slang_lookup_result = 'hahaha'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)
        mock_lookup_slang = mocker.patch('tululbot.commands.lookup_slang',
                                         return_value=slang_lookup_result,
                                         autospec=True)

        slang(fake_message)

        mock_lookup_slang.assert_called_once_with(slang_term)
        mock_reply_to.assert_called_once_with(fake_message, slang_lookup_result,
                                              parse_mode='Markdown')

    def test_slang_with_bot_name(self, mocker, fake_message):
        bot_username = 'somebot'
        slang_term = 'hohoi'
        fake_message.text = '/slang@{} {}'.format(bot_username, slang_term)
        slang_lookup_result = 'hahaha'
        mocker.patch('tululbot.commands.BOT_USERNAME', bot_username)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)
        mock_lookup_slang = mocker.patch('tululbot.commands.lookup_slang',
                                         return_value=slang_lookup_result,
                                         autospec=True)

        slang(fake_message)

        mock_lookup_slang.assert_called_once_with(slang_term)
        mock_reply_to.assert_called_once_with(fake_message, slang_lookup_result,
                                              parse_mode='Markdown')

    def test_slang_no_term(self, mocker, fake_message):
        fake_message.text = '/slang'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        slang(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Apa yang mau dicari jir?',
                                              force_reply=True)


def test_hotline(fake_message, mocker):
    fake_message.text = '/hotline'
    mock_hotline_message_id = mocker.patch('tululbot.commands.HOTLINE_MESSAGE_ID',
                                           autospec=True)
    mock_forward_message = mocker.patch('tululbot.commands.bot.forward_message', autospec=True)

    hotline(fake_message)

    mock_forward_message.assert_called_once_with(fake_message.chat.id, fake_message.chat.id,
                                                 mock_hotline_message_id)


class TestHbdCommand:

    def test_hbd(self, mocker, fake_message):
        fake_name = 'Tutu Lulul'
        fake_message.text = '/hbd {}'.format(fake_name)
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(fake_name)
        mock_send_message = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

        hbd(fake_message)

        mock_send_message.assert_called_once_with(fake_message.chat.id, greetings)

    def test_hbd_with_bot_name(self, mocker, fake_message):
        bot_username = 'somebot'
        fake_name = 'Tutu Lulul'
        fake_message.text = '/hbd@{} {}'.format(bot_username, fake_name)
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(fake_name)
        mocker.patch('tululbot.commands.BOT_USERNAME', bot_username)
        mock_send_message = mocker.patch('tululbot.commands.bot.send_message')

        hbd(fake_message)

        mock_send_message.assert_called_once_with(fake_message.chat.id, greetings)

    def test_hbd_no_word(self, mocker, fake_message):
        fake_message.text = '/hbd'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        hbd(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Siapa yang ultah?',
                                              force_reply=True)
