import requests


def lookup_kbbi_definition(term):
    payload = {
        'format': 'json',
        'phrase': term
    }
    r = requests.get('http://kateglo.com/api.php', params=payload)
    r.raise_for_status()
    try:
        json_response = r.json()
    except ValueError:
        return []
    else:
        return [to_def(obj) for obj in json_response['kateglo']['definition']]


def to_def(obj):
    return {
        'class': obj['lex_class_ref'],
        'def_text': obj['def_text'],
        'sample': obj['sample']
    }


def format_def(i, dic):
    return '{}. {}{}\n{}'.format(i, dic['def_text'], format_class(dic['class']),
                                 format_sample(dic['sample']))


def format_class(cls):
    return ' (_{}_)'.format(cls) if cls else ''


def format_sample(sample):
    return '_{}_\n'.format(sample) if sample else ''
