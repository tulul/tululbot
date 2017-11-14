from os import environ
import warnings


APP_ENV = environ.get('APP_ENV', 'development')
DEBUG = environ.get('DEBUG', 'true') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', '')
LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST', '127.0.0.1')
HOTLINE_MESSAGE_ID = environ.get('HOTLINE_MESSAGE_ID')
TAMPOL_MESSAGE_ID = environ.get('TAMPOL_MESSAGE_ID')
TELEGRAM_BOT_USERNAME = environ.get('TELEGRAM_BOT_USERNAME', '')

try:
    TULULBOT_DEVEL_CHAT_ID = environ['TULULBOT_DEVEL_CHAT_ID']
except KeyError:
    warnings.warn('TULULBOT_DEVEL_CHAT_ID is not set; errors will pass silently')
    TULULBOT_DEVEL_CHAT_ID = ''
