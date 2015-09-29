import json
from unittest.mock import patch

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


def test_wiki_command_with_no_term(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'text': '/wiki',
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
    assert json_response['text'] == 'Masukin kata kunci pencarian lah'
    assert json_response['disable_web_page_preview'] == 'false'
    assert json_response['reply_to_message_id'] == 100


def test_wiki_command_with_term_whose_article_can_be_found(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 200
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/wiki tulul',
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
        assert json_response['text'] == 'http://en.wikipedia.org/wiki/tulul'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_wiki_command_with_term_whose_article_cannot_be_found(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 404
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/wiki tulul',
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
        assert json_response['text'] == 'Gak ada artikelnya. Jangan nge-lely.'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_wiki_command_but_other_error_happens(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 500
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/wiki tulul',
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
        assert json_response['text'] == 'Shit happens...'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_wiki_command_with_two_words_term(app):
    with patch('tululbot.requests') as mock_requests:
        mock_requests.get.return_value.status_code = 200
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/wiki too lulz',
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
        assert json_response['text'] == 'http://en.wikipedia.org/wiki/too_lulz'
        assert json_response['disable_web_page_preview'] == 'false'
        assert json_response['reply_to_message_id'] == 100


def test_ngelely_command_with_no_term(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'text': '/ngelely',
            'chat': {
                'id': 1
            }
        }
    }
    rv = app.post('/', data=json.dumps(payload),
                  content_type='application/json')
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_ngelely_command_with_term(app):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'text': '/ngelely too lulz',
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
    assert json_response['text'] == ('Jangan nge-lely\n'
                                     'https://www.google.co.id/#q=too+lulz')
    assert json_response['disable_web_page_preview'] == 'false'
    assert json_response['reply_to_message_id'] == 100


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
        'telebot untuk tulul :v\n'
        'dibuat dengan Python 3.4 dan cinta\n'
        'baru bisa ngewiki dan ngelely doang\n'
        'kontribusi di https://github.com/tulul/tululbot'
    )
    assert json_response['text'] == expected_text
    assert json_response['disable_web_page_preview'] == 'false'
    assert json_response['reply_to_message_id'] == 100
