from datetime import datetime
from unittest.mock import patch

import pytest

from tululbot.utils import QuoteEngine

generic_quote_1 = (
    '--- '
    'quotes: '
    '  - q_no: 1'
    '    quote: "Kenapa kalo mau sahur tiba2 ngantuk? Karena Anda belum punya cinta yang menemani Anda sahur."'  # noqa
    '    author: Anang Ferdi'
    '    author_bio: Dokter cinta veteran'
    '    tags: '
    '      - cinta'
    '      - sahur'
    '      - ramadhan'
)

generic_quote_2 = (
    '---'
    'quotes:'
    '  - q_no: 3'
    '    quote: "Cinta itu bisa dibagi dengan 0 ga sih?"'
    '    author: Adrian Nuradiansyah'
    '    author_bio: Awesome Akhi'
    '    tags: '
    '      - cinta'
    '      - geek'
    '      - matematika '
)


@pytest.fixture
def qe():
    return QuoteEngine()


def test_refresh_time(qe):
    with patch('tululbot.utils.TimeHelper') as mock_dt:
        with patch('tululbot.utils.requests') as mock_requests:
            class FakeResponse:
                def get_json(self):
                    return self.json

                pass

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

            result = qe.refresh_url_if_applicable()
            assert result is True
            result = qe.refresh_url_if_applicable()
            assert result is False
            result = qe.refresh_url_if_applicable()
            assert result is False

            qe._last_refresh = datetime(2000, 1, 6, 15, 8, 24)

            result = qe.refresh_url_if_applicable()
            assert result is True
            result = qe.refresh_url_if_applicable()
            assert result is False
