'''from page_analyzer.url_processing import (
    error_message_1,
    error_message_2,
    error_message_3,
    normalize_url,
    validate_url,
)


sample1 = 'https://e1.ru/news/politics'
sample2 = 'http://mail.ru'
sample3 = ''
sample4 = 'just_a_string'
sample5 = 'https://' + 'test' + '.com' + 'x' * 256


def test_normalize_url():
    assert normalize_url(sample1) == 'https://e1.ru'
    assert normalize_url(sample2) == sample2
    assert normalize_url(sample3) == '://'


def test_validate_url():
    assert validate_url(sample1) == []
    assert validate_url(sample2) == []
    assert validate_url(sample3) == [error_message_1]
    assert validate_url(sample4) == [error_message_2]
    assert validate_url(sample5) == [error_message_3]'''
