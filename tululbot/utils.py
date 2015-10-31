from datetime import datetime
import random

import requests
import yaml


class TimeHelper:

    @classmethod
    def now():
        return datetime.datetime.now()


class QuoteEngine:

    def __init__(self):
        # Note: rawgit does not have 100% uptime, but at
        # least they're not throttling us.
        self._quote_url = 'https://cdn.rawgit.com/tulul/tulul-quotes/master/quote.yaml'  # noqa

        # Why not using rawgit's development endpoint? Because
        # they can't promise 100% uptime on the development endpoint.
        # Meanwhile, production endpoint's uptime is better because
        # it is served by MaxCDN
        self._git_branch_check_url = 'https://api.github.com/repos/tulul/tulul-quotes/branches/master'  # noqa

        self._cache = []

        # URI refresh per interval in seconds
        self._refresh_interval = 5 * 60
        # Dummy date. Must be old enough (just to trigger)
        # the uri must be refreshed on the first call
        self._last_refresh = datetime(2009, 1, 6, 15, 8, 24, 78915)

    def retrieve_random(self):
        cache = self._cache
        return self.format_quote(random.choice(cache))

    def format_quote(self, q):
        return '{q[quote]} - {q[author]}, {q[author_bio]}'.format(q=q)

    def refresh_cache_if_applicable(self):
        if (not self.refresh_url_if_applicable()):
            return False

        body = requests.get(self._quote_url).text
        # What if previously we have the cache, but this time
        # when we try to get new cache, the network occurs error?
        # We will think about "don't refresh if error" later.
        self._cache = yaml.load(body)['quotes']

        return True

    def refresh_url_if_applicable(self):
        now = TimeHelper.now()
        delta = now - self._last_refresh

        if (delta.seconds < self._refresh_interval):
            return False

        res = requests.get(self._git_branch_check_url)

        # Don't care broken request
        if (not res.ok):
            return False

        json = res.get_json()
        sha = json['commit']['sha']
        self._quote_url = 'https://cdn.rawgit.com/tulul/tulul-quotes/{}/quote.yaml'.format(sha)

        self._last_refresh = now

        return True
