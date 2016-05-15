import pytest

from tululbot.types import Message, Update, User


@pytest.fixture
def client():
    """Return Flask test client that is configured for testing.

    Testing configuration should be placed in `tests/.env` file.
    """
    from tululbot import app
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def fake_chat_dict():
    """Return a fake, minimalist Telegram chat as dict."""
    return {
        'id': 123,
        'type': 'group'
    }


@pytest.fixture
def fake_message_dict(fake_chat_dict):
    """Return a fake, minimalist Telegram message as dict."""
    return {
        'message_id': 12345,
        'date': 1445207090,
        'chat': fake_chat_dict
    }


@pytest.fixture
def fake_update_dict(fake_message_dict):
    """Return a fake Telegram update with message as dict."""
    return {
        'update_id': 12345,
        'message': fake_message_dict
    }


@pytest.fixture
def fake_message(fake_message_dict):
    """Return a fake, minimalist Telegram message."""
    return Message.from_dict(fake_message_dict)


@pytest.fixture
def fake_update(fake_update_dict):
    """Return a fake Telegram update with message."""
    return Update.from_dict(fake_update_dict)


@pytest.fixture
def fake_user_dict():
    """Return a fake, minimalist Telegram user as dict."""
    return {
        'id': 12345,
        'first_name': 'John'
    }


@pytest.fixture
def fake_user(fake_user_dict):
    """Return a fake, minimalist Telegram user."""
    return User.from_dict(fake_user_dict)
