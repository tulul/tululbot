import logging
from os import environ

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['DEBUG'] = environ.get('DEBUG') == 'true'

# Telegram configuration
TOKEN = environ['TELEGRAM_BOT_TOKEN']

# Why do this? See https://core.telegram.org/bots/api#setwebhook
BASE_PATH = '/{}'.format(TOKEN)

# Configure logging
LOG_LEVEL = environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=getattr(logging, LOG_LEVEL))


def wiki(term):
    """Return a wiki link and the first paragraph of the page."""

    search_term = term.replace(' ', '_')
    url = 'http://en.wikipedia.org/wiki/{}'.format(search_term)
    r = requests.get(url)
    if r.status_code == 200:
        return '{}'.format(url)
    elif r.status_code == 404:
        return 'Gak ada artikelnya. Jangan nge-lely.'
    else:
        return 'Shit happens...'


@app.route(BASE_PATH, methods=['POST'])
def main():
    body = request.get_json()
    logging.debug('update_id is %s', body['update_id'])
    message = body.get('message')
    logging.debug('message is %s', message)
    if message is not None:
        text = message.get('text')
        logging.debug('text is %s', text)
        chat_id = message['chat']['id']
        logging.debug('chat_id is %s', chat_id)

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
                    google_url = 'https://www.google.co.id/#q={}'.format(term)
                    return reply('Jangan nge-lely\n{}'.format(google_url))
            elif text == '/who':
                about_text = (
                    'telebot untuk tulul :v\n'
                    'dibuat dengan Python 3.4 dan cinta\n'
                    'baru bisa ngewiki dan ngelely doang\n'
                    'kontribusi di https://bitbucket.org/iqbalmineraltown/tululbot/'
                )
                return reply(about_text)

    return 'Nothing to do here...'


if __name__ == '__main__':
    app.run()
