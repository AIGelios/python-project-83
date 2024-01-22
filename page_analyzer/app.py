import os
from dotenv import load_dotenv

import requests
from flask import Flask, render_template, redirect, url_for, request
from requests.exceptions import RequestException
from psycopg2.errors import UniqueViolation

from .url_processing import normalize_url, validate_url
from .service_module import (
    error_alert,
    info_alert,
    done_alert,
    get_alerts,
    get_seo_data,
)
from .db_queries import (
    get_all_urls,
    add_new_url,
    get_url_id_by_name,
    get_url_by_id,
    get_checks_by_url_id,
    get_url_name_by_id,
    add_new_check,
)

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    ''' main page constructor '''
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    ''' urls page constructor '''
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    ''' add new url to database and redirect to url page '''
    url_string = request.form.get('url')
    errors = validate_url(url_string)
    if errors:
        for error in errors:
            error_alert(error)
        return render_template(
            'index.html',
            url=url_string,
            messages=get_alerts(),
        ), 422
    url_name = normalize_url(url_string)
    try:
        add_new_url(url_name)
        done_alert('Страница успешно добавлена')
    except UniqueViolation:
        info_alert('Страница уже существует')
    id = get_url_id_by_name(url_name)
    return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    ''' url page constructor '''
    url = get_url_by_id(id)
    if not url:
        return render_template('page_not_found.html'), 404
    checks = get_checks_by_url_id(id)
    return render_template(
        'url.html',
        url=url,
        checks=checks,
        messages=get_alerts(),
    )


@app.post('/urls/<int:id>/checks')
def add_check(id):
    ''' add check of url to database and redirect to url page '''
    url_name = get_url_name_by_id(id)
    try:
        response = requests.get(url_name, timeout=(3.05, 10))
        response.raise_for_status()
        status_code = response.status_code
        done_alert('Страница успешно проверена')
    except RequestException:
        error_alert('Произошла ошибка при проверке')
        return redirect(url_for('get_url', id=id))
    h1, title, description = get_seo_data(response.text)
    add_new_check(id, h1, title, description, status_code)
    return redirect(url_for('get_url', id=id))
