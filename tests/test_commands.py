from unittest.mock import call

from tululbot.commands import leli, quote, who


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
        'TululBot v1.0.1\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    mock_reply_to.assert_called_once_with(
        fake_message, expected_text, disable_preview=True
    )
