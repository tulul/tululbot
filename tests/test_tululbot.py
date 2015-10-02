import json
from unittest.mock import patch

import pytest

from tululbot.decorators import CommandNotFoundError


@pytest.fixture
def client():
    """Return Flask test client that is configured for testing.

    Testing configuration should be placed in `tests/.env` file.
    """
    from tululbot import app
    app.config['TESTING'] = True
    return app.test_client()


def do_post(client, payload):
    config = client.application.config
    base_path = '/{}'.format(config['TELEGRAM_BOT_TOKEN'])
    return client.post(base_path, data=json.dumps(payload),
                       content_type='application/json')


def test_no_message(client):
    payload = dict(update_id=12345)
    rv = do_post(client, payload)
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_no_text(client):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 100,
            'chat': {
                'id': 1
            }
        }
    }
    rv = do_post(client, payload)
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_no_matching_command(client):
    with patch('tululbot.dispatcher') as mock_dispatcher:
        mock_dispatcher.run_command.side_effect = CommandNotFoundError
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/toolulzwuow',
                'chat': {
                    'id': 1
                }
            }
        }

        rv = do_post(client, payload)
        assert rv.status_code == 200
        assert rv.get_data(as_text=True) == 'Nothing to do here...'


def test_command_returning_text(client):
    with patch('tululbot.dispatcher') as mock_dispatcher:
        mock_dispatcher.run_command.return_value = 'and_dan_dros'
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/toolulzwuow',
                'chat': {
                    'id': 1
                }
            }
        }

        rv = do_post(client, payload)
        assert rv.status_code == 200
        json_response = json.loads(rv.get_data(as_text=True))
        expected_response = {
            'method': 'sendMessage',
            'chat_id': 1,
            'text': 'and_dan_dros',
            'disable_web_page_preview': 'false',
            'reply_to_message_id': 100
        }
        assert json_response == expected_response


def test_command_with_disable_preview(client):
    with patch('tululbot.dispatcher') as mock_dispatcher:
        mock_dispatcher.run_command.return_value = ('and_dan_dros', True)
        payload = {
            'update_id': 12345,
            'message': {
                'message_id': 100,
                'text': '/toolulzwuow',
                'chat': {
                    'id': 1
                }
            }
        }

        rv = do_post(client, payload)
        assert rv.status_code == 200
        json_response = json.loads(rv.get_data(as_text=True))
        expected_response = {
            'method': 'sendMessage',
            'chat_id': 1,
            'text': 'and_dan_dros',
            'disable_web_page_preview': 'true',
            'reply_to_message_id': 100
        }
        assert json_response == expected_response
