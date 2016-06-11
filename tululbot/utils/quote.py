import random

import requests
import yaml


class QuoteEngine:

    def __init__(self):
        self.quote_url = 'https://raw.githubusercontent.com/tulul/tulul-quotes/master/quote.yaml'  # noqa
        # Note: rawgit does not have 100% uptime, but at
        # least they're not throttling us.

        self.cache = []

    def retrieve_random(self):
        if not self.cache:
            self.refresh_cache()

        return self.format_quote(random.choice(self.cache))

    def format_quote(self, q):
        return '{q[quote]} - {q[author]}, {q[author_bio]}'.format(q=q)

    def refresh_cache(self):
        r = requests.get(self.quote_url)
        r.raise_for_status()
        body = r.text
        # What if previosuly we have the cache, but this time
        # when we try to get new cache, the network occurs error?
        # We will think about "don't refresh if error" later.
        self.cache = yaml.load(body)['quotes']
