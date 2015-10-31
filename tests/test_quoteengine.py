from datetime import datetime
from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

from tululbot.utils import QuoteEngine


class FakeResponse:
    def get_json(self):
        return self.json

    pass


@pytest.fixture
def qe():
    return QuoteEngine()


def cdn_with_branch(branch):
    return 'https://cdn.rawgit.com/tulul/tulul-quotes/{}/quote.yaml'.format(branch)  # noqa


def test_refresh_time(qe):
    with patch('tululbot.utils.TimeHelper') as mock_dt:
        with patch('tululbot.utils.requests') as mock_requests:
            response1 = FakeResponse()
            response1.status_code = 200
            response1.json = {
                "commit": {
                    "sha": "beefbeef"
                }
            }

            response1.ok = True

            mock_requests.get.return_value = response1

            qe._refresh_interval = 5

            mock_dt.now.return_value = datetime(2009, 1, 6, 15, 8, 30)
            qe._last_refresh = datetime(2000, 1, 6, 15, 8, 24)

            assert qe._quote_url == cdn_with_branch("master")

            result = qe.refresh_url_if_applicable()
            assert result is True
            result = qe.refresh_url_if_applicable()
            assert result is False
            result = qe.refresh_url_if_applicable()
            assert result is False

            assert qe._quote_url == cdn_with_branch("beefbeef")

            qe._last_refresh = datetime(2000, 1, 6, 15, 8, 24)

            result = qe.refresh_url_if_applicable()
            assert result is True
            result = qe.refresh_url_if_applicable()
            assert result is False


def test_refresh_response(qe):
    with patch('tululbot.utils.requests') as mock_requests:

        # Test: stay empty if no need to refresh
        qe.refresh_url_if_applicable = MagicMock()
        qe.refresh_url_if_applicable.return_value = False

        qe.refresh_cache_if_applicable()

        assert qe._cache == []

        # Test: should refresh
        qe.refresh_url_if_applicable.return_value = True
        mock_requests.get.return_value = generic_quote_1
        qe.refresh_cache_if_applicable()
        result = qe.retrieve_random()
        assert result == 'Yuzu kok lucu banget sih - Waza, Pejuang'

        # Test: Remote content changed but no need to refresh
        qe.refresh_url_if_applicable.return_value = False
        mock_requests.get.return_value = generic_quote_2
        qe.refresh_cache_if_applicable()
        result = qe.retrieve_random()
        assert result == 'Yuzu kok lucu banget sih - Waza, Pejuang'

        # Test: Remote content changed and it does refresh
        qe.refresh_url_if_applicable.return_value = True
        mock_requests.get.return_value = generic_quote_2
        qe.refresh_cache_if_applicable()
        result = qe.retrieve_random()
        assert result == 'Miki Hoshii is the best girl - Waza, Rocket Builder'


generic_quote_1 = FakeResponse()
generic_quote_1.text = '''
---
quotes: \n
  - q_no: 1
    quote: "Yuzu kok lucu banget sih"
    author: Waza
    author_bio: Pejuang
    tags:
      - cinta
      - sahur
      - ramadhan
'''

generic_quote_2 = FakeResponse()
generic_quote_2.text = '''
---
quotes:
  - q_no: 3
    quote: "Miki Hoshii is the best girl"
    author: Waza
    author_bio: Rocket Builder
    tags:
      - cinta
      - geek
      - matematika
'''
