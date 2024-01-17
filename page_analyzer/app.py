from flask import (Flask, render_template)


import os
import psycopg2
from psycopg2.extras import NamedTupleConnection
from dotenv import load_dotenv

from .url_processing import normalize_url, validate_url  # noqa
from .date_and_time import get_current_timestamp  # noqa


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SESSION_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    path = './page_analyzer/db_queries/get_urls.sql'
    with open(path) as file:
        query = file.read()

    db_connection = psycopg2.connect(
        DATABASE_URL,
        connection_factory=NamedTupleConnection,
    )
    cursor = db_connection.cursor()

    cursor.execute(query)
    urls = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    pass


@app.get('/urls/<int:id>')
def get_url(id):
    pass


@app.post('/urls/<int:id>/checks')
def get_checks(id):
    pass
