from os import environ
from urllib.parse import urlencode

from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from QuoteEngine import QuoteEngine


def create_app(config_dict):
    app = Flask(__name__)

    # Configure the app. This factory pattern is useful for
    # testing so we don't have to put testing config in a separate file.
    app.config.update(config_dict)

    # Why do this? See https://core.telegram.org/bots/api#setwebhook
    base_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])

    # Configure application logging
    app.logger.setLevel(app.config['LOG_LEVEL'])

    quote_engine = QuoteEngine()
    quote_engine.refresh_cache()

    def leli(term):
        """
        Return the first paragraph of a relevant page on Wikipedia,
        or a google search link if no relevant pages found.
        """

        def search_on_wikipedia():
            def has_result(page):
                return 'Search results' not in page

            def parse_content_text(page):
                return BeautifulSoup(page).find('div', id='mw-content-text')

            def parse_first_paragraph(page):
                return parse_content_text(page).find('p').get_text()

            def has_disambiguations(paragraph):
                return 'may refer to:' in paragraph

            def parse_first_disambiguation_link(page):
                def valid_link(tag):
                    return tag.name == 'a' and tag['href'].startswith('/wiki')

                path = parse_content_text(page).find(valid_link)['href']
                return 'https://en.wikipedia.org{}'.format(path)

            query_string = urlencode(dict(search=term))
            search_url = \
                'https://en.wikipedia.org/w/index.php?{}'.format(query_string)

            response = requests.get(search_url)
            if response.status_code != 200:
                return None

            page = response.text
            if not has_result(page):
                return None

            first_paragraph = parse_first_paragraph(page)
            if not has_disambiguations(first_paragraph):
                return first_paragraph

            disambiguation_url = parse_first_disambiguation_link(page)

            response = requests.get(disambiguation_url)
            if response.status_code != 200:
                return None

            disambiguated_page = response.text
            return parse_first_paragraph(disambiguated_page)

        def search_on_google():
            query_string = urlencode(dict(q=term))
            search_url = 'https://google.com/search?{}'.format(query_string)
            return 'Jangan ngeleli! Googling dong: {}'.format(search_url)

        result = search_on_wikipedia()
        return result if result is not None else search_on_google()

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
                if text.startswith('/leli'):
                    term = text[6:]
                    if not term:
                        return reply('Apa yang mau dileli?')
                    return reply(leli(term))
                elif text.startswith('/quote'):
                    return reply(quote_engine.retrieve_random())
                elif text == '/who':
                    about_text = (
                        'TululBot v0.1.0\n\n'
                        'Enhancing your tulul experience since 2015\n\n'
                        'Contribute on https://github.com/tulul/tululbot\n\n'
                        "We're hiring! Contact @iqbalmineraltown for details"
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
