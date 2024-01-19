from flask import Flask, render_template, redirect, url_for, request

import os
from dotenv import load_dotenv
'''
import psycopg2
from psycopg2.extras import NamedTupleCursor
'''
from psycopg2.errors import UniqueViolation
from requests import get as make_http_request
from requests.exceptions import RequestException

from .url_processing import normalize_url, validate_url

from .db_connections import exec_query

from .service_module import (
    error_alert,
    info_alert,
    done_alert,
    get_alerts,
    get_seo_data,
)
from .db_queries import (
    get_all_urls_query,
    add_url_query,
    get_id_by_url_query,
    get_url_data_by_id_query,
    add_check_query,
    get_checks_by_url_id,
    get_url_by_id_query,
)

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
'''
DATABASE_URL = os.getenv('DATABASE_URL')


def make_connection():
    return psycopg2.connect(DATABASE_URL)


def exec_query(query, with_data_return=True):
    with make_connection() as conn:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query)
        if with_data_return:
            data = cursor.fetchall()
        cursor.close()
    return data if with_data_return else None
'''


@app.route('/')
def index():
    ''' main page constructor '''
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    ''' urls page constructor '''
    query = get_all_urls_query()
    urls = exec_query(query)
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    ''' add new url to database and redirect to url page '''
    url_string = request.form.get('url')
    if (errors := validate_url(url_string)):
        for error in errors:
            error_alert(error)
        return render_template(
            'index.html',
            url=url_string,
            messages=get_alerts(),
        )
    url = normalize_url(url_string)
    try:
        query = add_url_query(url)
        exec_query(query, False)
        done_alert('Страница успешно добавлена')
    except UniqueViolation:
        info_alert('Страница уже существует')
    query = get_id_by_url_query(url)
    id = exec_query(query)[0].id
    return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    ''' url page constructor '''
    query = get_url_data_by_id_query(id)
    data = exec_query(query)
    if data:
        url = data[0]
        query = get_checks_by_url_id(id)
        checks = exec_query(query)
        return render_template(
            'url.html',
            url=url,
            checks=checks,
            messages=get_alerts(),
        )
    return render_template('page_not_found.html'), 404


@app.post('/urls/<int:id>/checks')
def add_check(id):
    ''' add check of url to database and redirect to url page '''
    query = get_url_by_id_query(id)
    url = exec_query(query)[0].name
    try:
        response = make_http_request(url, timeout=(3.05, 10))
        response.raise_for_status()
        status_code = response.status_code
        done_alert('Страница успешно проверена')
    except RequestException:
        error_alert('Произошла ошибка при проверке')
        return redirect(url_for('get_url', id=id))
    h1, title, description = get_seo_data(response.text)
    query = add_check_query(id, h1, title, description, status_code)
    exec_query(query, False)
    return redirect(url_for('get_url', id=id))
