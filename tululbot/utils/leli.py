from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests


def search_on_wikipedia(term):
    search_url = 'https://en.wikipedia.org/w/index.php'

    response = requests.get(search_url, params=dict(search=term))
    response.raise_for_status()

    page = response.text
    if not has_result(page):
        return None

    first_paragraph = parse_first_paragraph(page)
    if not has_disambiguations(first_paragraph.get_text()):
        return first_paragraph.get_text()

    disambiguation_url = parse_first_disambiguation_link(page)

    response = requests.get(disambiguation_url)
    response.raise_for_status()

    disambiguated_page = response.text
    return parse_first_paragraph(disambiguated_page).get_text()


def parse_first_disambiguation_link(page):
    def valid_link(tag):
        return tag.name == 'a' and tag['href'].startswith('/wiki')

    path = parse_content_text(page).find(valid_link)['href']
    return 'https://en.wikipedia.org{}'.format(path)


def has_disambiguations(paragraph):
    return 'may refer to:' in paragraph


def has_result(page):
    return ('Search results' not in page and
            parse_first_paragraph(page) is not None)


def parse_first_paragraph(page):
    return parse_content_text(page).find('p')


def parse_content_text(page):
    return BeautifulSoup(page, 'html.parser').find('div', id='mw-content-text')


def search_on_google(term):
    query_string = urlencode(dict(q=term))
    search_url = 'https://google.com/search?{}'.format(query_string)
    return 'Jangan ngeleli! Googling dong: {}'.format(search_url)
