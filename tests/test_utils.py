from telebot import types

from tululbot.utils import TululBot


class TestTululBot:

    def test_user_property(self, mocker, fake_user):
        bot = TululBot('TOKEN')
        mock_get_me = mocker.patch.object(bot, 'get_me', autospec=True,
                                          return_value=fake_user)

        rv = bot.user

        assert rv == fake_user
        mock_get_me.assert_called_once_with()

    def test_create_is_reply_to_filter(self, mocker, fake_message_dict, fake_user_dict):
        fake_replied_message_dict = fake_message_dict.copy()

        fake_message = types.Message.de_json(fake_message_dict)
        fake_replied_message = types.Message.de_json(fake_replied_message_dict)

        bot_user = types.User.de_json(fake_user_dict)
        bot_message = 'Message text from bot goes here'
        fake_replied_message.text = bot_message
        fake_replied_message.from_user = bot_user
        fake_message.reply_to_message = fake_replied_message

        bot = TululBot('TOKEN')
        bot.user = bot_user

        assert bot.create_is_reply_to_filter(bot_message)(fake_message)
        assert not bot.create_is_reply_to_filter('foo bar')(fake_message)
