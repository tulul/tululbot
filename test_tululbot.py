import json
from unittest.mock import patch, call

import pytest

from tululbot import create_app


@pytest.fixture
def app():
    """Return TululBot application object that is configured for testing."""
    test_config = {
        'DEBUG': False,
        'TELEGRAM_BOT_TOKEN': '',
        'LOG_LEVEL': 'WARNING',
        'TESTING': True
    }
    app = create_app(test_config)
    return app.test_client()


def test_no_message(app):
    payload = dict(update_id=12345)
    rv = app.post('/', data=json.dumps(payload),
                  content_type='application/json')
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_no_text(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'chat': {
                'id': 1
            }
        }
    }
    rv = app.post('/', data=json.dumps(payload),
                  content_type='application/json')
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_leli_command_with_no_term(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'text': '/leli',
            'chat': {
                'id': 1
            }
        }
    }
    rv = app.post('/', data=json.dumps(payload),
                  content_type='application/json')
    assert rv.status_code == 200
    json_response = json.loads(rv.get_data(as_text=True))
    assert json_response['method'] == 'sendMessage'
    assert json_response['chat_id'] == 1
    assert json_response['text'] == 'Apa yang mau dileli?'
    assert json_response['disable_web_page_preview'] == 'false'
    assert json_response['reply_to_message_id'] == 100


def test_leli_command_with_term_found_on_wikipedia(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = (
            '<html>'
            '    <div id="mw-content-text">'
            '        <p>Tulul is the synonym of cool.</p>'
            '    </div>'
            '</html>'
        )
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/leli tulul',
                'chat': {
                    'id': 1
                }
            }
        }
        rv = app.post('/', data=json.dumps(payload),
                      content_type='application/json')

        mock_requests.get.assert_called_once_with(
            'https://en.wikipedia.org/w/index.php?search=tulul'
        )

        assert rv.status_code == 200
        json_response = json.loads(rv.get_data(as_text=True))
        assert json_response['method'] == 'sendMessage'
        assert json_response['chat_id'] == 1
        assert json_response['text'] == 'Tulul is the synonym of cool.'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_leli_command_with_ambiguous_term_on_wikipedia(app):
    with patch('tululbot.requests') as mock_requests:
        class FakeResponse(object):
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

        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/leli snowden',
                'chat': {
                    'id': 1
                }
            }
        }
        rv = app.post('/', data=json.dumps(payload),
                      content_type='application/json')

        assert mock_requests.get.call_args_list == [
            call('https://en.wikipedia.org/w/index.php?search=snowden'),
            call('https://en.wikipedia.org/wiki/link1')
        ]

        assert rv.status_code == 200
        json_response = json.loads(rv.get_data(as_text=True))
        assert json_response['method'] == 'sendMessage'
        assert json_response['chat_id'] == 1
        assert json_response['text'] == 'Snowden is former CIA employee.'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_leli_command_with_term_resorted_on_google(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = (
            '<html>'
            '<h1>Search results</h1>'
            '</html>'
        )
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/leli wazaundtechnik',
                'chat': {
                    'id': 1
                }
            }
        }
        rv = app.post('/', data=json.dumps(payload),
                      content_type='application/json')

        mock_requests.get.assert_called_once_with(
            'https://en.wikipedia.org/w/index.php?search=wazaundtechnik'
        )

        assert rv.status_code == 200
        json_response = json.loads(rv.get_data(as_text=True))
        assert json_response['method'] == 'sendMessage'
        assert json_response['chat_id'] == 1
        assert json_response['text'] == (
            'Jangan ngeleli! Googling dong: '
            'https://google.com/search?q=wazaundtechnik'
        )
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_leli_command_with_multiword_term(app):
    with patch('tululbot.requests') as mock_requests:
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/leli waza und technik',
                'chat': {
                    'id': 1
                }
            }
        }
        app.post('/', data=json.dumps(payload),
                 content_type='application/json')

        mock_requests.get.assert_called_once_with(
            'https://en.wikipedia.org/w/index.php?search=waza+und+technik'
        )


def test_who_command(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'text': '/who',
            'chat': {
                'id': 1
            }
        }
    }
    rv = app.post('/', data=json.dumps(payload),
                  content_type='application/json')
    assert rv.status_code == 200
    json_response = json.loads(rv.get_data(as_text=True))
    assert json_response['method'] == 'sendMessage'
    assert json_response['chat_id'] == 1
    expected_text = (
        'TululBot v0.1.0\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    assert json_response['text'] == expected_text
    assert json_response['disable_web_page_preview'] == 'false'
    assert json_response['reply_to_message_id'] == 100
