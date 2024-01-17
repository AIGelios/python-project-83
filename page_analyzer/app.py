from flask import Flask, render_template, redirect, url_for
from flask import request, flash, get_flashed_messages

import os
from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extras import NamedTupleConnection
from psycopg2.errors import UniqueViolation

from .url_processing import normalize_url, validate_url  # noqa
# from .service_module import get_current_timestamp
from .db_queries import get_urls_query, insert_url_query, get_url_id_query


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SESSION_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html',
        url='',
        messages=[]
    )


@app.get('/urls')
def get_urls():

    query = get_urls_query()

    factory = NamedTupleConnection
    db_connection = connect(DATABASE_URL, connection_factory=factory)

    cursor = db_connection.cursor()
    cursor.execute(query)
    urls = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    url_string = request.form.get('url')
    errors = validate_url(url_string)

    if errors:
        for error in errors:
            flash(error, 'alert-danger')
        return render_template(
            'index.html',
            url=url_string,
            messages=get_flashed_messages(with_categories=True),
        )

    url = normalize_url(url_string)

    try:
        db_connection = connect(DATABASE_URL)
        cursor = db_connection.cursor()
        query = insert_url_query(url)
        cursor.execute(query)
        flash('Страница успешно добавлена', 'alert-success')
        db_connection.commit()
        cursor.close()
        db_connection.close()
    except UniqueViolation:
        flash('Страница уже существует', 'alert-info')
    db_connection = connect(DATABASE_URL)
    cursor = db_connection.cursor()
    query = get_url_id_query(url)
    cursor.execute(query)
    id = cursor.fetchone()[0]
    db_connection.commit()
    cursor.close()
    db_connection.close()
    return render_template(
        'index.html',
        url=f'page with id {id}',
        messages=get_flashed_messages(with_categories=True),
    )


@app.get('/urls/<int:id>')
def get_url(id):
    return f'Данные по странице {id}'


@app.post('/urls/<int:id>/checks')
def get_checks(id):
    return redirect(url_for('index'))
