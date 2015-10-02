from os import environ
import warnings


DEBUG = environ.get('DEBUG') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', '')
LOG_LEVEL = environ.get('LOG_LEVEL', 'WARNING')

try:
    TULULBOT_DEVEL_CHAT_ID = environ['TULULBOT_DEVEL_CHAT_ID']
except KeyError:
    warnings.warn('TULULBOT_DEVEL_CHAT_ID is not set; errors will pass silently')
    TULULBOT_DEVEL_CHAT_ID = ''
