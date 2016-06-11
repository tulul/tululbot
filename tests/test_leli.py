from tululbot.utils.leli import search_on_wikipedia, search_on_google


def test_search_on_wikipedia_and_found(mocker):
    mock_requests = mocker.patch('tululbot.utils.leli.requests', autospec=True)

    mock_requests.get.return_value.text = (
        '<html>'
        '    <div id="mw-content-text">'
        '        <p>Tulul is the synonym of cool.</p>'
        '    </div>'
        '</html>'
    )

    rv = search_on_wikipedia('tulul')

    assert rv == 'Tulul is the synonym of cool.'


def test_ambiguous_term_on_wikipedia(mocker):
    mock_requests = mocker.patch('tululbot.utils.leli.requests', autospec=True)

    class FakeResponse:
        def __init__(self, text):
            self.text = text

        def raise_for_status(self):
            pass

    response1_text = (
        '<html>'
        '    <div id="mw-content-text">'
        '        <p>Snowden may refer to:</p>'
        '        <ul>'
        '            <li><a href="/wiki/link1">Snowden1</a></li>'
        '            <li><a href="/wiki/link2">Snowden2</a></li>'
        '        </ul>'
        '    </div>'
        '</html>'
    )
    response1 = FakeResponse(response1_text)

    response2_text = (
        '<html>'
        '    <div id="mw-content-text">'
        '        <p>Snowden is former CIA employee.</p>'
        '    </div>'
        '</html>'
    )
    response2 = FakeResponse(response2_text)

    mock_requests.get.side_effect = [response1, response2]

    rv = search_on_wikipedia('snowden')

    assert rv == 'Snowden is former CIA employee.'


def test_search_on_google():
    rv = search_on_google('wazaundtechnik')

    expected_text = (
        'Jangan ngeleli! Googling dong: '
        'https://google.com/search?q=wazaundtechnik'
    )
    assert rv == expected_text
