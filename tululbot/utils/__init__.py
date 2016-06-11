from telebot import TeleBot, types


class TululBot(TeleBot):

    def __init__(self, token):
        super(TululBot, self).__init__(token)
        self._user = None

    @property
    def user(self):
        if self._user is not None:
            return self._user

        self._user = self.get_me()
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def reply_to(self, *args, **kwargs):
        try:
            force_reply = kwargs.pop('force_reply')
        except KeyError:
            return super(TululBot, self).reply_to(*args, **kwargs)
        else:
            if force_reply:
                kwargs['reply_markup'] = types.ForceReply(selective=True)
            return super(TululBot, self).reply_to(*args, **kwargs)

    def create_is_reply_to_filter(self, text):
        def is_reply_to_bot(message):
            return (self.is_reply_to_bot_user(message) and
                    message.reply_to_message.text == text)

        return is_reply_to_bot

    def is_reply_to_bot_user(self, message):
        replied_message = message.reply_to_message
        return (replied_message is not None and
                replied_message.from_user is not None and
                replied_message.from_user.id == self.user.id)
