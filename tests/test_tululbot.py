import json


def do_post(client, payload, content_type='application/json'):
    config = client.application.config
    base_path = '/{}'.format(config['TELEGRAM_BOT_TOKEN'])
    return client.post(base_path, data=json.dumps(payload),
                       content_type=content_type)


def test_not_json_content(client):
    payload = {
        'name': 'Foo',
        'address': 'bar'
    }
    rv = do_post(client, payload, content_type='application/x-www-form-urlencoded')

    assert rv.status_code == 403


def test_valid_update(client, mocker, fake_update_dict):
    mock_handle_new_message = mocker.patch('tululbot.bot.handle_new_message',
                                           autospec=True)

    rv = do_post(client, fake_update_dict)

    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'OK'
    assert mock_handle_new_message.called
