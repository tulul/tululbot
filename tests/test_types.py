from tululbot.types import Message, Chat, Update, User


def test_create_chat_from_dict(fake_chat_dict):
    chat = Chat.from_dict(fake_chat_dict)

    assert chat.id == fake_chat_dict['id']
    assert chat.type == fake_chat_dict['type']


def test_create_message_from_dict(fake_message_dict):
    fake_message_dict['text'] = 'Foo bar'
    message = Message.from_dict(fake_message_dict)

    assert message.message_id == fake_message_dict['message_id']
    assert message.date == fake_message_dict['date']
    assert message.chat.id == fake_message_dict['chat']['id']
    assert message.chat.type == fake_message_dict['chat']['type']
    assert message.text == fake_message_dict['text']
    assert not hasattr(message, 'reply_to_message')
    assert message.from_user is None


def test_create_reply_message_from_dict(fake_message_dict):
    fake_reply_message_dict = fake_message_dict.copy()

    fake_message_dict['text'] = 'Foo bar'
    fake_reply_message_dict['text'] = 'Baz quux'
    fake_reply_message_dict['reply_to_message'] = fake_message_dict
    reply_message = Message.from_dict(fake_reply_message_dict)

    assert hasattr(reply_message, 'reply_to_message')
    replied_message = reply_message.reply_to_message
    assert replied_message.message_id == fake_message_dict['message_id']
    assert replied_message.text == fake_message_dict['text']


def test_create_update_from_dict(fake_update_dict):
    update = Update.from_dict(fake_update_dict)

    assert update.update_id == fake_update_dict['update_id']
    assert update.message.message_id == fake_update_dict['message']['message_id']
    assert update.message.date == fake_update_dict['message']['date']
    assert update.message.chat.id == fake_update_dict['message']['chat']['id']
    assert update.message.chat.type == fake_update_dict['message']['chat']['type']


def test_create_user_from_dict(fake_user_dict):
    user = User.from_dict(fake_user_dict)

    assert user.id == fake_user_dict['id']
    assert user.first_name == fake_user_dict['first_name']
