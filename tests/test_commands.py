from requests.exceptions import HTTPError, ConnectionError

from tululbot.commands import leli, quote, who, slang, hotline, hbd, kbbi, eid, xmas, kawin


class TestLeliCommand:

    def test_no_term(self, mocker, fake_message):
        fake_message.text = '/leli'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Apa yang mau dileli?',
                                              force_reply=True)

    def test_term_found_on_wikipedia(self, fake_message, mocker):
        fake_message.text = '/leli tulul'
        fake_rv = 'foo bar'
        mocker.patch('tululbot.commands.search_on_wikipedia', return_value=fake_rv,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, fake_rv,
                                              disable_web_page_preview=True)

    def test_term_resorted_on_google(self, fake_message, mocker):
        fake_message.text = '/leli wazaundtechnik'
        fake_rv = 'baz quux'
        mocker.patch('tululbot.commands.search_on_wikipedia', return_value=None,
                     autospec=True)
        mocker.patch('tululbot.commands.search_on_google', return_value=fake_rv,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, fake_rv,
                                              disable_web_page_preview=True)

    def test_term_only(self, mocker, fake_message):
        fake_message.text = 'foo bar'
        mock_search = mocker.patch('tululbot.commands.search_on_wikipedia', autospec=True)
        mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_search.assert_called_once_with(fake_message.text)

    def test_http_error(self, mocker, fake_message):
        fake_message.text = '/leli asdf asdf'
        mocker.patch('tululbot.commands.search_on_wikipedia', side_effect=HTTPError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Aduh ada error nich')

    def test_conn_error(self, mocker, fake_message):
        fake_message.text = '/leli asdf asdf'
        mocker.patch('tululbot.commands.search_on_wikipedia', side_effect=ConnectionError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        leli(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, "Koneksi lagi bapuk nih :'(")


class TestQuoteCommand:

    def test_quote(self, fake_message, mocker):
        fake_message.text = '/quote'
        mock_engine = mocker.patch('tululbot.commands.quote_engine', autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)
        mock_engine.retrieve_random.return_value = 'some random quote'

        quote(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'some random quote')

    def test_http_error(self, fake_message, mocker):
        fake_message.text = '/quote'
        mocker.patch('tululbot.commands.quote_engine.retrieve_random', side_effect=HTTPError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        quote(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Aduh ada error nich')

    def test_conn_error(self, fake_message, mocker):
        fake_message.text = '/quote'
        mocker.patch('tululbot.commands.quote_engine.retrieve_random',
                     side_effect=ConnectionError, autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        quote(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, "Koneksi lagi bapuk nih :'(")


def test_who(fake_message, mocker):
    fake_message.text = '/who'
    mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

    who(fake_message)

    expected_text = (
        'TululBot v1.10.0\n\n'
        'Enhancing your tulul experience since 2015\n\n'
        'Contribute on https://github.com/tulul/tululbot\n\n'
        "We're hiring! Contact @iqbalmineraltown for details"
    )
    mock_reply_to.assert_called_once_with(fake_message, expected_text,
                                          disable_web_page_preview=True)


class TestSlangCommand:

    def test_slang(self, mocker, fake_message):
        slang_term = 'hohoi ahoi'
        fake_message.text = '/slang {}'.format(slang_term)
        slang_lookup_result = 'hahaha'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)
        mock_lookup_slang = mocker.patch('tululbot.commands.lookup_slang',
                                         return_value=slang_lookup_result,
                                         autospec=True)

        slang(fake_message)

        mock_lookup_slang.assert_called_once_with(slang_term)
        mock_reply_to.assert_called_once_with(fake_message, slang_lookup_result,
                                              parse_mode='Markdown')

    def test_no_term(self, mocker, fake_message):
        fake_message.text = '/slang'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        slang(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Apa yang mau dicari jir?',
                                              force_reply=True)

    def test_term_only(self, mocker, fake_message):
        fake_message.text = 'foo bar'
        mock_lookup = mocker.patch('tululbot.commands.lookup_slang', autospec=True)
        mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        slang(fake_message)

        mock_lookup.assert_called_once_with(fake_message.text)

    def test_http_error(self, mocker, fake_message):
        fake_message.text = '/slang asdf asdf'
        mocker.patch('tululbot.commands.lookup_slang', side_effect=HTTPError, autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        slang(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Aduh ada error nich')

    def test_conn_error(self, mocker, fake_message):
        fake_message.text = '/slang asdf asdf'
        mocker.patch('tululbot.commands.lookup_slang', side_effect=ConnectionError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        slang(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, "Koneksi lagi bapuk nih :'(")


class TestHotline:

    def test_hotline(self, fake_message, mocker):
        fake_message.text = '/hotline'
        fake_hotline_message_id = 123
        mocker.patch('tululbot.commands.HOTLINE_MESSAGE_ID', fake_hotline_message_id)
        mock_forward_message = mocker.patch('tululbot.commands.bot.forward_message',
                                            autospec=True)

        hotline(fake_message)

        mock_forward_message.assert_called_once_with(fake_message.chat.id,
                                                     fake_message.chat.id,
                                                     fake_hotline_message_id)

    def test_no_hotline_message_id_set(self, fake_message, mocker):
        fake_message.text = '/hotline'
        mocker.patch('tululbot.commands.HOTLINE_MESSAGE_ID', None)
        mock_forward_message = mocker.patch('tululbot.commands.bot.forward_message',
                                            autospec=True)

        hotline(fake_message)

        assert not mock_forward_message.called


class TestHbdCommand:

    def test_hbd(self, mocker, fake_message):
        fake_name = 'Tutu Lulul'
        fake_message.text = '/hbd {}'.format(fake_name)
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(fake_name)
        mock_send_message = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

        hbd(fake_message)

        mock_send_message.assert_called_once_with(fake_message.chat.id, greetings)

    def test_no_word(self, mocker, fake_message):
        fake_message.text = '/hbd'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        hbd(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Siapa yang ultah?',
                                              force_reply=True)

    def test_word_only(self, mocker, fake_message):
        fake_message.text = 'foo bar'
        greetings_format = ('hoi {}'
                            ' met ultah ya moga sehat dan sukses selalu '
                            '\U0001F389 \U0001F38A')
        greetings = greetings_format.format(fake_message.text)
        mock_send = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

        hbd(fake_message)

        mock_send.assert_called_once_with(fake_message.chat.id, greetings)


class TestKBBICommand:

    def test_kbbi(self, mocker, fake_message):
        fake_message.text = '/kbbi foo bar'
        fake_rv = [
            {
                'class': 'nomina',
                'def_text': 'baz quux',
                'sample': 'baz baz quux quux'
            },
            {
                'class': 'adjektiva',
                'def_text': 'quux baz',
                'sample': None
            }
        ]
        mocker.patch('tululbot.commands.lookup_kbbi_definition', return_value=fake_rv,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        expected_text = ('1. baz quux (_nomina_)\n'
                         '_baz baz quux quux_\n'
                         '\n'
                         '2. quux baz (_adjektiva_)\n')
        mock_reply_to.assert_called_once_with(fake_message, expected_text,
                                              parse_mode='Markdown')

    def test_no_defs(self, mocker, fake_message):
        fake_message.text = '/kbbi foo bar'
        mocker.patch('tululbot.commands.lookup_kbbi_definition', return_value=[],
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Gak ada bray')

    def test_no_term(self, mocker, fake_message):
        fake_message.text = '/kbbi'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Cari apa lu?', force_reply=True)

    def test_term_only(self, mocker, fake_message):
        fake_message.text = 'foo bar'
        mock_lookup = mocker.patch('tululbot.commands.lookup_kbbi_definition', autospec=True)
        mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        mock_lookup.assert_called_once_with(fake_message.text)

    def test_http_error(self, mocker, fake_message):
        fake_message.text = '/kbbi asdf asdf'
        mocker.patch('tululbot.commands.lookup_kbbi_definition', side_effect=HTTPError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Aduh ada error nich')

    def test_conn_error(self, mocker, fake_message):
        fake_message.text = '/kbbi asdf asdf'
        mocker.patch('tululbot.commands.lookup_kbbi_definition', side_effect=ConnectionError,
                     autospec=True)
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kbbi(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, "Koneksi lagi bapuk nih :'(")


class TestKawinCommand:

    def test_kawin(self, mocker, fake_message, fake_user):
        fake_message.text = '/kawin mpid'
        fake_message.from_user = fake_user
        mock_send_message = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

        kawin(fake_message)

        expected_message = ('Hoi mpid selamat nikah & kawin ya! '
                            'Semoga jadi keluarga yang bahagia. '
                            'Semoga lancar semuanya sampai enna-enna. '
                            'Dari {} dan keluarga.'.format(fake_user.first_name))
        mock_send_message.assert_called_once_with(fake_message.chat.id, expected_message)

    def test_no_couple(self, mocker, fake_message):
        fake_message.text = '/kawin'
        mock_reply_to = mocker.patch('tululbot.commands.bot.reply_to', autospec=True)

        kawin(fake_message)

        mock_reply_to.assert_called_once_with(fake_message, 'Siapa yang mau kawin jir?', force_reply=True)

def test_eid_command(mocker, fake_message, fake_user):
    fake_message.text = '/eid'
    fake_message.from_user = fake_user
    mock_send_message = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

    eid(fake_message)

    expected_message = ('Taqabbalallahu minna wa minkum, shiyaamana wa shiyaamakum. '
                        'Mohon maaf lahir dan batin ya guys. '
                        'Dari {} dan keluarga.'.format(fake_user.first_name))
    mock_send_message.assert_called_once_with(fake_message.chat.id, expected_message)


def test_xmas_command(mocker, fake_message, fake_user):
    fake_message.text = '/xmas'
    fake_message.from_user = fake_user
    mock_send_message = mocker.patch('tululbot.commands.bot.send_message', autospec=True)

    xmas(fake_message)

    expected_message = ('Selamat natal semua! '
                        'Dari {} dan keluarga.'.format(fake_user.first_name))
    mock_send_message.assert_called_once_with(fake_message.chat.id, expected_message)
