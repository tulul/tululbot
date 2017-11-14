import traceback

from flask import Flask, abort, request
app = Flask(__name__)
app.config.from_object('{}.config'.format(__name__))

from telebot import types  # noqa: E402

from tululbot.utils import TululBot  # noqa: E402
bot = TululBot(app.config['TELEGRAM_BOT_TOKEN'])  # Must be before importing commands

from tululbot import commands  # noqa


# Why do this? See https://core.telegram.org/bots/api#setwebhook
webhook_url_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])
webhook_url_base = app.config['WEBHOOK_HOST']

app.logger.setLevel(app.config['LOG_LEVEL'])


@app.route(webhook_url_path, methods=['POST'])
def main():
    json_data = request.get_json(silent=True)
    if json_data is not None:
        update = types.Update.de_json(json_data)
        app.logger.debug('Get an update with id %s', update.update_id)
        if update.message is not None:
            app.logger.debug('Get message with id: %s, content: %s',
                             update.message.message_id,
                             update.message.text)
            bot.process_new_messages([update.message])
        return 'OK'
    else:
        abort(403)


@app.errorhandler(500)
def handle_uncaught_exception(error):  # pragma: no cover
    if app.config['TULULBOT_DEVEL_CHAT_ID']:
        chat_id = app.config['TULULBOT_DEVEL_CHAT_ID']
        bot.send_message(chat_id, traceback.format_exc())

    return 'OK'


if app.config['APP_ENV'] != 'development':  # pragma: no cover
    bot.set_webhook('{}{}'.format(webhook_url_base, webhook_url_path))
