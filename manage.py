#!/usr/bin/env python

import code
from os import environ
from os.path import join, dirname
import subprocess
import sys

import click
from dotenv import load_dotenv
import pytest
import requests


def load_app():
    # Environment variable MUST be set before importing the app
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    from tululbot import app
    return app


@click.group()
def manage():
    """Script to manage tasks outside the application itself."""
    pass


@manage.command()
def shell():
    """Run a shell with custom context."""
    context = dict(app=load_app())
    try:
        from IPython import embed
    except ImportError:
        code.interact(local=context)
    else:
        embed(user_ns=context)


@manage.command()
def runserver():
    """Run the application server."""
    load_app().run()


@manage.command()
def test():
    """Run the tests."""
    # Environment variable MUST be set before importing the app
    dotenv_path = join(dirname(__file__), 'tests', '.env')
    load_dotenv(dotenv_path)

    sys.exit(pytest.main([]))


@manage.command()
def lint():
    """Run the linters."""
    sys.exit(subprocess.call(['flake8']))


@manage.command()
def check():
    """Run linters and tests.

    Use this command to check before making a pull request."""
    # Environment variable MUST be set before importing the app
    dotenv_path = join(dirname(__file__), 'tests', '.env')
    load_dotenv(dotenv_path)

    sys.exit(subprocess.call(['flake8']) or pytest.main([]))


@manage.command()
@click.argument('message')
def notify(message):
    """Send notification to TululBot developers group."""
    token = environ['TELEGRAM_BOT_TOKEN']
    telegram_bot_api_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    payload = {
        'chat_id': environ['TULULBOT_DEVEL_CHAT_ID'],
        'text': message
    }
    resp = requests.post(telegram_bot_api_url, data=payload)
    res = resp.json()
    if res['ok']:
        print('Notification successfully sent')
    else:
        print('ERROR:', res['description'], file=sys.stderr)


if __name__ == '__main__':
    manage()
