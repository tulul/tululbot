from requests.exceptions import ConnectionError, HTTPError

from tululbot import app, bot
from tululbot.utils.kbbi import format_def, lookup_kbbi_definition
from tululbot.utils.quote import QuoteEngine
from tululbot.utils.slang import lookup_slang
from tululbot.utils.leli import search_on_google, search_on_wikipedia


quote_engine = QuoteEngine()
HOTLINE_MESSAGE_ID = app.config['HOTLINE_MESSAGE_ID']
BOT_USERNAME = app.config['TELEGRAM_BOT_USERNAME']


@bot.message_handler(func=bot.create_is_reply_to_filter('Apa yang mau dileli?'))
@bot.message_handler(regexp=r'^/leli(@{})?( .+)*$'.format(BOT_USERNAME))
def leli(message):
    app.logger.debug('Detected leli command {!r}'.format(message.text))
    try:
        if message.text.startswith('/leli'):
            _, term = message.text.split(' ', maxsplit=1)
        else:
            term = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Apa yang mau dileli?', force_reply=True)
    else:
        app.logger.debug('Extracted leli term {!r}'.format(term))
        try:
            result = search_on_wikipedia(term)
        except HTTPError:
            bot.reply_to(message, 'Aduh ada error nich')
        except ConnectionError:
            bot.reply_to(message, "Koneksi lagi bapuk nih :'(")
        else:
            if result is None:
                result = search_on_google(term)
            bot.reply_to(message, result, disable_web_page_preview=True)


@bot.message_handler(regexp=r'^/quote(@{})?$'.format(BOT_USERNAME))
def quote(message):
    app.logger.debug('Detected quote command {!r}'.format(message.text))
    try:
        random_quote = quote_engine.retrieve_random()
    except HTTPError:
        bot.reply_to(message, 'Aduh ada error nich')
    except ConnectionError:
        bot.reply_to(message, "Koneksi lagi bapuk nih :'(")
    else:
        bot.reply_to(message, random_quote)


@bot.message_handler(regexp=r'^/who(@{})?$'.format(BOT_USERNAME))
def who(message):
    app.logger.debug('Detected who command {!r}'.format(message.text))
    about_text = (
        'TululBot v1.11.2\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    return bot.reply_to(message, about_text, disable_web_page_preview=True)


@bot.message_handler(func=bot.create_is_reply_to_filter('Apa yang mau dicari jir?'))
@bot.message_handler(regexp=r'^/slang(@{})?( .+)*$'.format(BOT_USERNAME))
def slang(message):
    app.logger.debug('Detected slang command {!r}'.format(message.text))
    try:
        if message.text.startswith('/slang'):
            _, term = message.text.split(' ', maxsplit=1)
        else:
            term = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Apa yang mau dicari jir?', force_reply=True)
    else:
        try:
            definition = lookup_slang(term)
        except HTTPError:
            bot.reply_to(message, 'Aduh ada error nich')
        except ConnectionError:
            bot.reply_to(message, "Koneksi lagi bapuk nih :'(")
        else:
            app.logger.debug('Extracted slang term {!r}'.format(term))
            bot.reply_to(message, definition, parse_mode='Markdown')


@bot.message_handler(regexp=r'^/hotline(@{})?$'.format(BOT_USERNAME))
def hotline(message):
    app.logger.debug('Detected hotline command {!r}'.format(message.text))
    if HOTLINE_MESSAGE_ID is not None:
        bot.forward_message(message.chat.id, message.chat.id, HOTLINE_MESSAGE_ID)


@bot.message_handler(func=bot.create_is_reply_to_filter('Siapa yang ultah?'))
@bot.message_handler(regexp=r'^/hbd(@{})?( @?\w+)*$'.format(BOT_USERNAME))
def hbd(message):
    app.logger.debug('Detected hbd command {!r}'.format(message.text))
    try:
        if message.text.startswith('/hbd'):
            _, name = message.text.split(' ', maxsplit=1)
        else:
            name = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Siapa yang ultah?', force_reply=True)
    else:
        app.logger.debug('Extracted hbd name {!r}'.format(name))
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(name)
        bot.send_message(message.chat.id, greetings)


@bot.message_handler(func=bot.create_is_reply_to_filter('Cari apa lu?'))
@bot.message_handler(regexp=r'^/kbbi(@{})?( \w+)*$'.format(BOT_USERNAME))
def kbbi(message):
    app.logger.debug('Detected kbbi command {!r}'.format(message.text))
    try:
        if message.text.startswith('/kbbi'):
            _, term = message.text.split(' ', maxsplit=1)
        else:
            term = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Cari apa lu?', force_reply=True)
    else:
        app.logger.debug('Extracted kbbi term {!r}'.format(term))
        try:
            defs = lookup_kbbi_definition(term)
        except HTTPError:
            bot.reply_to(message, 'Aduh ada error nich')
        except ConnectionError:
            bot.reply_to(message, "Koneksi lagi bapuk nih :'(")
        else:
            if defs:
                response = '\n'.join(format_def(i, d) for i, d in enumerate(defs, start=1))
                bot.reply_to(message, response, parse_mode='Markdown')
            else:
                bot.reply_to(message, 'Gak ada bray')


@bot.message_handler(regexp=r'^/eid(@{})?$'.format(BOT_USERNAME))
def eid(message):
    app.logger.debug('Detected eid command {!r}'.format(message.text))
    eid_greeting = ('Taqabbalallahu minna wa minkum, shiyaamana wa shiyaamakum. '
                    'Mohon maaf lahir dan batin ya guys. '
                    'Dari {} dan keluarga.'.format(message.from_user.first_name))
    bot.send_message(message.chat.id, eid_greeting)


@bot.message_handler(regexp=r'^/xmas(@{})?$'.format(BOT_USERNAME))
def xmas(message):
    app.logger.debug('Detected xmas command {!r}'.format(message.text))
    xmas_greeting = ('Selamat natal semua! '
                     'Dari {} dan keluarga.'.format(message.from_user.first_name))
    bot.send_message(message.chat.id, xmas_greeting)


@bot.message_handler(func=bot.create_is_reply_to_filter('Siapa yang mau kawin jir?'))
@bot.message_handler(regexp=r'^/kawin(@{})?( .+)*$'.format(BOT_USERNAME))
def kawin(message):
    app.logger.debug('Detected kawin command {!r}'.format(message.text))
    try:
        if message.text.startswith('/kawin'):
            _, couple = message.text.split(' ', maxsplit=1)
        else:
            couple = message.text
    except ValueError:
        app.logger.debug('Cannot split text {!r}'.format(message.text))
        bot.reply_to(message, 'Siapa yang mau kawin jir?', force_reply=True)
    else:
        app.logger.debug('Extracted kawin couple {!r}'.format(couple))
        kawin_greeting = ('Hoi {} selamat nikah & kawin ya! '
                          'Semoga jadi keluarga yang bahagia. '
                          'Semoga lancar semuanya sampai enna-enna. '
                          'Dari {} dan keluarga.'.format(couple, message.from_user.first_name))
        bot.send_message(message.chat.id, kawin_greeting)
