from telebot import types


class WrapperClassMixin:

    @classmethod
    def from_dict(cls, the_dict):
        return cls.wrapped_class.de_json(the_dict)


class Chat(WrapperClassMixin):
    wrapped_class = types.Chat


class Message(WrapperClassMixin):
    wrapped_class = types.Message


class Update(WrapperClassMixin):
    wrapped_class = types.Update


class User(WrapperClassMixin):
    wrapped_class = types.User
