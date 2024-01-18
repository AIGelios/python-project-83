from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
)

import os
from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from psycopg2.errors import UniqueViolation

from .url_processing import normalize_url, validate_url  # noqa
from .service_module import (
    error_alert,
    info_alert,
    done_alert,
    get_alerts,
)
from .db_queries import (
    get_all_urls_query,
    add_url_query,
    get_id_by_url_query,
    get_url_data_by_id_query,
    add_check_query,
    get_checks_by_url_id,
)

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SESSION_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    db_connection = connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template(
        'index.html',
        url='',
        messages=[]
    )


@app.get('/urls')
def get_urls():
    query = get_all_urls_query()
    with db_connection:
        cursor = db_connection.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query)
        urls = cursor.fetchall()
        cursor.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():

    url_string = request.form.get('url')
    errors = validate_url(url_string)

    if errors:
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
        with db_connection:
            cursor = db_connection.cursor()
            cursor.execute(query)
            cursor.close()
            done_alert('Страница успешно добавлена')

    except UniqueViolation:
        info_alert('Страница уже существует')

    query = get_id_by_url_query(url)
    with db_connection:
        cursor = db_connection.cursor()
        cursor.execute(query)
        id = cursor.fetchone()[0]
        cursor.close()
    return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):

    query = get_url_data_by_id_query(id)

    with db_connection:
        cursor = db_connection.cursor()
        cursor.execute(query)
        matched = cursor.fetchone()
        cursor.close()

    if matched:
        url_id, url_name, created_at = matched
        created_at = str(created_at.date())

        query = get_checks_by_url_id(id)

        with db_connection:
            cursor = db_connection.cursor(cursor_factory=NamedTupleCursor)
            cursor.execute(query)
            checks = cursor.fetchall()
            cursor.close()

        return render_template(
            'url.html',
            url_id=url_id,
            url_name=url_name,
            created_at=created_at,
            checks=checks,
            messages=get_alerts(),
        )

    return render_template('page_not_found.html'), 404


@app.post('/urls/<int:id>/checks')
def add_check(id):

    h1 = ''
    title = ''
    description = ''
    status_code = 200

    query = add_check_query(id, h1, title, description, status_code)

    with db_connection:
        cursor = db_connection.cursor()
        cursor.execute(query)
        cursor.close()
        done_alert('Страница успешно проверена')

    return redirect(url_for('get_url', id=id))
