from datetime import datetime
from flask import flash, get_flashed_messages
from bs4 import BeautifulSoup


def get_current_timestamp():
    return datetime.now()


def error_alert(message):
    flash(message, 'alert-danger')


def done_alert(message):
    flash(message, 'alert-success')


def info_alert(message):
    flash(message, 'alert-info')


def get_alerts():
    return get_flashed_messages(with_categories=True)


def get_seo_data(html_document):
    soup = BeautifulSoup(html_document, 'html.parser')
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    desc_with_tag = soup.find('meta', {'name': 'description'})
    desc = desc_with_tag['content'] if desc_with_tag else ''
    desc = desc if len(desc) < 255 else desc[:252] + '...'
    return h1, title, desc
