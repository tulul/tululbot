import pytest
from telebot import types

from tululbot.utils import TululBot
from tululbot.types import Message


def test_create_bot():
    bot = TululBot('TOKEN')

    assert bot._telebot is not None
    assert bot.user is None


def test_get_me(mocker):
    bot = TululBot('TOKEN')
    mock_get_me = mocker.patch.object(bot._telebot, 'get_me', autospec=True)

    bot.get_me()

    mock_get_me.assert_called_once_with()
    assert bot.user is not None


def test_send_message(mocker):
    bot = TululBot('TOKEN')
    return_value = 'some return value'
    mock_send_message = mocker.patch.object(bot._telebot, 'send_message',
                                            return_value=return_value,
                                            autospec=True)
    chat_id = 12345
    text = 'Hello world'

    rv = bot.send_message(chat_id, text)

    assert rv == return_value
    mock_send_message.assert_called_once_with(chat_id, text)


def test_set_webhook(mocker):
    bot = TululBot('TOKEN')
    return_value = 'some return value'
    webhook_url = 'some url'
    mock_set_webhook = mocker.patch.object(bot._telebot, 'set_webhook',
                                           return_value=return_value, autospec=True)

    rv = bot.set_webhook(webhook_url)

    assert rv == return_value
    mock_set_webhook.assert_called_once_with(webhook_url)


def test_reply_to(mocker, fake_message):
    bot = TululBot('TOKEN')
    return_value = 'some return value'
    mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to',
                                        return_value=return_value,
                                        autospec=True)
    text = 'Hello world'

    rv = bot.reply_to(fake_message, text)

    assert rv == return_value
    mock_reply_to.assert_called_once_with(fake_message, text,
                                          disable_web_page_preview=False,
                                          reply_markup=None)


def test_reply_to_with_preview_disabled(mocker, fake_message):
    bot = TululBot('TOKEN')
    mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to', autospec=True)
    text = 'Hello world'

    bot.reply_to(fake_message, text, disable_preview=True)

    mock_reply_to.assert_called_once_with(fake_message, text,
                                          disable_web_page_preview=True,
                                          reply_markup=None)


def test_reply_to_with_force_reply(mocker, fake_message):
    bot = TululBot('TOKEN')
    mock_reply_to = mocker.patch.object(bot._telebot, 'reply_to', autospec=True)
    text = 'dummy text'

    bot.reply_to(fake_message, text, force_reply=True)

    args, kwargs = mock_reply_to.call_args
    assert args == (fake_message, text)
    assert len(kwargs) == 2
    assert 'disable_web_page_preview' in kwargs
    assert not kwargs['disable_web_page_preview']
    assert 'reply_markup' in kwargs
    assert isinstance(kwargs['reply_markup'], types.ForceReply)


def test_message_handler_with_no_argument():
    bot = TululBot('TOKEN')
    with pytest.raises(ValueError):
        @bot.message_handler()
        def handle(message):
            pass


def test_equals_message_handler(mocker, fake_message):
    bot = TululBot('TOKEN')
    mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                               autospec=True)

    @bot.message_handler(equals='/hello')
    def handle(message):
        pass

    args, kwargs = mock_message_handler.call_args
    assert len(args) == 0
    assert len(kwargs) == 1
    assert 'func' in kwargs
    func = kwargs['func']
    fake_message.text = '/hello'
    assert func(fake_message)
    fake_message.text = '/hello world'
    assert not func(fake_message)


def test_is_reply_to_bot_message_handler(mocker, fake_message_dict, fake_user_dict):
    fake_reply_message_dict = fake_message_dict.copy()

    bot = TululBot('TOKEN')
    bot_id = 12345

    class FakeUser:
        def __init__(self, id):
            self.id = id

    bot.user = FakeUser(bot_id)
    mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                               autospec=True)

    fake_user_dict['id'] = bot_id
    bot_message = 'Hah?'
    fake_message_dict['text'] = bot_message
    fake_message_dict['from'] = fake_user_dict
    fake_reply_message_dict['reply_to_message'] = fake_message_dict
    fake_reply_message = Message.from_dict(fake_reply_message_dict)

    @bot.message_handler(is_reply_to_bot=bot_message)
    def handle(message):
        pass

    args, kwargs = mock_message_handler.call_args
    assert len(args) == 0
    assert len(kwargs) == 1
    assert 'func' in kwargs
    func = kwargs['func']
    assert func(fake_reply_message)


def test_is_reply_to_bot_message_handler_with_uninitialized_bot_user(mocker, fake_message):
    bot = TululBot('TOKEN')
    mock_get_me = mocker.patch.object(bot._telebot, 'get_me', autospec=True)
    mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler', autospec=True)

    @bot.message_handler(is_reply_to_bot='asdf')
    def handle(message):
        pass

    args, kwargs = mock_message_handler.call_args
    assert len(args) == 0
    assert len(kwargs) == 1
    assert 'func' in kwargs
    func = kwargs['func']
    func(fake_message)
    mock_get_me.assert_called_once_with()


def test_handle_new_message(mocker, fake_message):
    bot = TululBot('TOKEN')
    mock_process_new_messages = mocker.patch.object(bot._telebot, 'process_new_messages',
                                                    autospec=True)

    bot.handle_new_message(fake_message)

    mock_process_new_messages.assert_called_once_with([fake_message])


def test_commands_message_handler(mocker):
    bot = TululBot('TOKEN')
    mock_message_handler = mocker.patch.object(bot._telebot, 'message_handler',
                                               autospec=True)

    @bot.message_handler(commands=['hello'])
    def handle(message):
        pass

    args, kwargs = mock_message_handler.call_args
    assert len(args) == 0
    assert len(kwargs) == 1
    assert 'commands' in kwargs
    assert kwargs['commands'] == ['hello']
