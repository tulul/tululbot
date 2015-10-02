import traceback

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config.from_object('{}.config'.format(__name__))

from .commands import dispatcher
from .decorators import CommandNotFoundError


# Why do this? See https://core.telegram.org/bots/api#setwebhook
base_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])

# Configure application logging
app.logger.setLevel(app.config['LOG_LEVEL'])


@app.route(base_path, methods=['POST'])
def main():
    body = request.get_json()
    app.logger.debug('update_id is %s', body['update_id'])
    message = body.get('message')
    app.logger.debug('message is %s', message)
    if message is not None:
        text = message.get('text')
        app.logger.debug('text is %s', text)
        chat_id = message['chat']['id']
        app.logger.debug('chat_id is %s', chat_id)

        if text is not None:
            def reply(reply_text, disable_preview=False):
                payload = {
                    'method': 'sendMessage',
                    'chat_id': chat_id,
                    'text': reply_text,
                    'disable_web_page_preview':
                        'true' if disable_preview else 'false',
                    'reply_to_message_id': message['message_id']
                }
                return jsonify(**payload)

            try:
                res = dispatcher.run_command(text)
            except CommandNotFoundError:
                # Ignore if command not found
                return 'Nothing to do here...'
            else:
                if isinstance(res, tuple):
                    reply_text, disable_preview = res
                    return reply(reply_text, disable_preview=disable_preview)
                else:
                    return reply(res)
        else:
            return 'Nothing to do here...'
    else:
        return 'Nothing to do here...'


@app.errorhandler(500)
def handle_uncaught_exception(error):
    if app.config['TULULBOT_DEVEL_CHAT_ID']:
        token = app.config['TELEGRAM_BOT_TOKEN']
        telegram_bot_api_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
        payload = {
            'chat_id': app.config['TULULBOT_DEVEL_CHAT_ID'],
            'text': traceback.format_exc()
        }
        requests.post(telegram_bot_api_url, data=payload)

    return 'OK'
