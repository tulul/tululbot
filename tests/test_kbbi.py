from tululbot.utils.kbbi import lookup_kbbi_definition


def test_lookup_kbbi(mocker):
    class FakeResponse:
        def json(self):
            return {
                'kateglo': {
                    'definition': [
                        {
                            'lex_class_ref': 'nomina',
                            'def_text': 'foo bar',
                            'sample': 'foo bar foo bar'
                        },
                        {
                            'lex_class_ref': 'adjektiva',
                            'def_text': 'baz quux',
                            'sample': 'baz baz quux quux'
                        }
                    ]
                }
            }

        def raise_for_status(self):
            pass

    fake_term = 'asdf asdf'
    mock_get = mocker.patch('tululbot.utils.kbbi.requests.get', return_value=FakeResponse(),
                            autospec=True)

    rv = lookup_kbbi_definition(fake_term)

    assert len(rv) == 2
    assert {
        'class': 'nomina',
        'def_text': 'foo bar',
        'sample': 'foo bar foo bar'
    } in rv
    assert {
        'class': 'adjektiva',
        'def_text': 'baz quux',
        'sample': 'baz baz quux quux'
    } in rv
    mock_get.assert_called_once_with('http://kateglo.com/api.php',
                                     params={'format': 'json', 'phrase': fake_term})


def test_lookup_kbbi_term_not_found(mocker):
    class FakeResponse:
        def json(self):
            raise ValueError

        def raise_for_status(self):
            pass

    mocker.patch('tululbot.utils.kbbi.requests.get', return_value=FakeResponse(),
                 autospec=True)

    rv = lookup_kbbi_definition('asdf asdf')

    assert rv == []
