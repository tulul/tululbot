import traceback

from flask import Flask, request, abort
app = Flask(__name__)
app.config.from_object('{}.config'.format(__name__))

from .utils import TululBot
bot = TululBot(app.config['TELEGRAM_BOT_TOKEN'])  # Must be before importing commands

from . import commands  # noqa
from .types import Update


# Why do this? See https://core.telegram.org/bots/api#setwebhook
webhook_url_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])
webhook_url_base = app.config['WEBHOOK_HOST']

app.logger.setLevel(app.config['LOG_LEVEL'])


@app.route(webhook_url_path, methods=['POST'])
def main():
    if request.headers.get('content-type') == 'application/json':
        update = Update.from_dict(request.get_json())
        app.logger.debug('Get an update with id %s', update.update_id)
        if update.message is not None:
            bot.handle_new_message(update.message)
        return 'OK'
    else:
        abort(403)


@app.errorhandler(500)
def handle_uncaught_exception(error):
    if app.config['TULULBOT_DEVEL_CHAT_ID']:
        chat_id = app.config['TULULBOT_DEVEL_CHAT_ID']
        bot.send_message(chat_id, traceback.format_exc())

    return 'OK'


if app.config['APP_ENV'] != 'development':
    bot.set_webhook('{}{}'.format(webhook_url_base, webhook_url_path))
