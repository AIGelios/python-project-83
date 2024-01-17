from urllib.parse import urlparse as parse
from validators import url as is_valid


def normalize_url(url_string: str) -> str:
    url_obj = parse(url_string)
    return f'{url_obj.scheme}://{url_obj.netloc}'


error_message_1 = 'URL обязателен'
error_message_2 = 'Некорректный URL'
error_message_3 = 'URL превышает 255 символов'


def validate_url(url_string: str) -> list:
    if url_string == '':
        return [error_message_1]
    if not is_valid(url_string):
        return [error_message_2]
    if len(url_string) > 255:
        return [error_message_3]
