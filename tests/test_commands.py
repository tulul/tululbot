from unittest.mock import patch, call, Mock

import pytest

from tululbot.commands import dispatcher, leli, quote, who


@pytest.fixture
def mock_commands(request):
    """Return a dictionary of mocked bot commands."""
    original_command_list = dispatcher._command_list[:]
    progs, callbacks = zip(*original_command_list)
    mock_callbacks = [Mock()] * len(callbacks)

    dispatcher._command_list = zip(progs, mock_callbacks)

    def teardown():
        dispatcher._command_list = original_command_list
    request.addfinalizer(teardown)

    command_names = [cb.__name__ for cb in callbacks]
    return dict(zip(command_names, mock_callbacks))


class TestLeliCommand:

    def test_with_term_found_on_wikipedia(self):
        with patch('tululbot.commands.requests') as mock_requests:
            mock_requests.get.return_value.status_code = 200
            mock_requests.get.return_value.text = (
                '<html>'
                '    <div id="mw-content-text">'
                '        <p>Tulul is the synonym of cool.</p>'
                '    </div>'
                '</html>'
            )

            rv = leli('tulul')

            mock_requests.get.assert_called_once_with(
                'https://en.wikipedia.org/w/index.php?search=tulul'
            )
            assert isinstance(rv, tuple)
            assert len(rv) == 2
            text, disable_preview = rv
            assert text == 'Tulul is the synonym of cool.'
            assert disable_preview

    def test_with_ambiguous_term_on_wikipedia(self):
        with patch('tululbot.commands.requests') as mock_requests:
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

            rv = leli('snowden')

            assert mock_requests.get.call_args_list == [
                call('https://en.wikipedia.org/w/index.php?search=snowden'),
                call('https://en.wikipedia.org/wiki/link1')
            ]
            assert isinstance(rv, tuple)
            assert len(rv) == 2
            text, disable_preview = rv
            assert text == 'Snowden is former CIA employee.'
            assert disable_preview

    def test_with_term_resorted_on_google(self):
        with patch('tululbot.commands.requests') as mock_requests:
            mock_requests.get.return_value.status_code = 200
            mock_requests.get.return_value.text = (
                '<html>'
                '<h1>Search results</h1>'
                '</html>'
            )

            rv = leli('wazaundtechnik')

            mock_requests.get.assert_called_once_with(
                'https://en.wikipedia.org/w/index.php?search=wazaundtechnik'
            )
            assert isinstance(rv, tuple)
            assert len(rv) == 2
            text, disable_preview = rv
            assert text == (
                'Jangan ngeleli! Googling dong: '
                'https://google.com/search?q=wazaundtechnik'
            )
            assert disable_preview

    def test_with_one_term(self, mock_commands):
        mock_leli = mock_commands['leli']
        dispatcher.run_command('/leli mpid')
        mock_leli.assert_called_once_with('mpid')

    def test_with_multiword_term(self, mock_commands):
        mock_leli = mock_commands['leli']
        dispatcher.run_command('/leli waza und technik')
        mock_leli.assert_called_once_with('waza und technik')


def test_quote():
    with patch('tululbot.commands.quote_engine') as mock_engine:
        mock_engine.retrieve_random.return_value = 'some random quote'
        rv = quote()
        assert rv == 'some random quote'


def test_quote_command(mock_commands):
    mock_quote = mock_commands['quote']
    dispatcher.run_command('/quote')
    assert mock_quote.called


def test_who():
    rv = who()
    assert isinstance(rv, tuple)
    assert len(rv) == 2
    text, disable_preview = rv
    assert text == (
        'TululBot v0.1.0\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    assert disable_preview


def test_who_command(mock_commands):
    mock_who = mock_commands['who']
    dispatcher.run_command('/who')
    assert mock_who.called
