"""
Commands module containing all commands TululBot can perform.

A command is marked by `@dispatcher.command(regex_pattern)` decorator
where `regex_pattern` is a valid Python's regex pattern corresponding
to the command. Whenever an update arrives and its text matches a command's
regex pattern, the command will be invoked. If the regex pattern contains
a grouping pattern, the matching group will be passed as arguments to
the command.

A command should return text to be sent as reply to the update. Command may
also return a 2-tuple; the first component is the reply text and the second
component is a boolean indicating whether to disable web page preview.
"""
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

from .decorators import CommandDispatcher
from .utils import QuoteEngine


dispatcher = CommandDispatcher()

quote_engine = QuoteEngine()


@dispatcher.command(r'^/leli (?P<term>.+)$')
def leli(term):
    """Search the given term on the internet.

    Return the first paragraph of a relevant page on Wikipedia,
    or a google search link if no relevant pages found.
    """

    def search_on_wikipedia():
        def parse_content_text(page):
            return BeautifulSoup(page).find('div', id='mw-content-text')

        def parse_first_paragraph(page):
            return parse_content_text(page).find('p')

        def has_result(page):
            return ('Search results' not in page and
                    parse_first_paragraph(page) is not None)

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
        if not has_disambiguations(first_paragraph.get_text()):
            return first_paragraph.get_text()

        disambiguation_url = parse_first_disambiguation_link(page)

        response = requests.get(disambiguation_url)
        if response.status_code != 200:
            return None

        disambiguated_page = response.text
        return parse_first_paragraph(disambiguated_page).get_text()

    def search_on_google():
        query_string = urlencode(dict(q=term))
        search_url = 'https://google.com/search?{}'.format(query_string)
        return 'Jangan ngeleli! Googling dong: {}'.format(search_url)

    result = search_on_wikipedia()
    if result is not None:
        return result, True
    else:
        return search_on_google(), True


@dispatcher.command(r'^/quote$')
def quote():
    quote_engine.refresh_cache_if_applicable()
    return quote_engine.retrieve_random()


@dispatcher.command(r'^/who$')
def who():
    about_text = (
        'TululBot v0.1.0\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    return about_text, True
