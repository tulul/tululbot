from os import environ
import warnings


APP_ENV = environ.get('APP_ENV', 'development')
DEBUG = environ.get('DEBUG') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', '')
LOG_LEVEL = environ.get('LOG_LEVEL', 'WARNING')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST', '127.0.0.1')

try:
    TULULBOT_DEVEL_CHAT_ID = environ['TULULBOT_DEVEL_CHAT_ID']
except KeyError:
    warnings.warn('TULULBOT_DEVEL_CHAT_ID is not set; errors will pass silently')
    TULULBOT_DEVEL_CHAT_ID = ''
