from os import environ
from urllib.parse import urlencode

from flask import Flask, request, jsonify
import requests


def create_app(config_dict):
    app = Flask(__name__)

    # Configure the app. This factory pattern is useful for
    # testing so we don't have to put testing config in a separate file.
    app.config.update(config_dict)

    # Why do this? See https://core.telegram.org/bots/api#setwebhook
    base_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])

    # Configure application logging
    app.logger.setLevel(app.config['LOG_LEVEL'])

    def wiki(term):
        """Return a wiki link for the term."""
        search_term = term.replace(' ', '_')
        url = 'http://en.wikipedia.org/wiki/{}'.format(search_term)
        r = requests.get(url)
        if r.status_code == 200:
            return '{}'.format(url)
        elif r.status_code == 404:
            return 'Gak ada artikelnya. Jangan nge-lely.'
        else:
            return 'Shit happens...'

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

            def reply(reply_text):
                payload = {
                    'method': 'sendMessage',
                    'chat_id': chat_id,
                    'text': reply_text,
                    'disable_web_page_preview': 'false',
                    'reply_to_message_id': message['message_id']
                }
                return jsonify(**payload)

            if text is not None:
                if text.startswith('/wiki'):
                    term = text[6:]
                    if term:
                        return reply(wiki(term))
                    return reply('Masukin kata kunci pencarian lah')
                elif text.startswith('/ngelely'):
                    term = text[9:]
                    if term:
                        qs = urlencode(dict(q=term))
                        google_url = 'https://www.google.co.id/#{}'.format(qs)
                        return reply('Jangan nge-lely\n{}'.format(google_url))
                elif text == '/who':
                    about_text = (
                        'telebot untuk tulul :v\n'
                        'dibuat dengan Python 3.4 dan cinta\n'
                        'baru bisa ngewiki dan ngelely doang\n'
                        'kontribusi di https://github.com/tulul/tululbot'
                    )
                    return reply(about_text)
        return 'Nothing to do here...'

    return app

default_config = {
    'DEBUG': environ.get('DEBUG') == 'true',
    'TELEGRAM_BOT_TOKEN': environ.get('TELEGRAM_BOT_TOKEN', ''),
    'LOG_LEVEL': environ.get('LOG_LEVEL', 'WARNING')
}

default_app = create_app(default_config)

if __name__ == '__main__':
    default_app.run()
