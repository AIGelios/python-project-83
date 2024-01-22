import os
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    get_flashed_messages,
)
from .db_interface import (
    get_all_urls,
    add_new_url,
    get_url_id_by_name,
    get_url_by_id,
    get_checks_by_url_id,
    get_url_name_by_id,
    add_new_check,
    url_already_exists_error,
)
from .url_processing import normalize_url, validate_url
from .html_parsing import get_seo_data, request_error


app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    raw_url = request.form.get('url')
    errors = validate_url(raw_url)
    if errors:
        for error in errors:
            flash(error, 'alert-danger')
        return render_template(
            'index.html',
            url=raw_url,
            messages=get_flashed_messages(with_categories=True),
        ), 422
    url_name = normalize_url(raw_url)
    try:
        add_new_url(url_name)
        flash('Страница успешно добавлена', 'alert-success')
    except url_already_exists_error:
        flash('Страница уже существует', 'alert-info')
    id = get_url_id_by_name(url_name)
    return redirect(url_for('get_url', id=id))


@app.get('/urls/<int:id>')
def get_url(id):
    url = get_url_by_id(id)
    checks = get_checks_by_url_id(id)
    return render_template(
        'url.html',
        url=url,
        checks=checks,
        messages=get_flashed_messages(with_categories=True),
    )


@app.post('/urls/<int:id>/checks')
def add_check(id):
    url_name = get_url_name_by_id(id)
    try:
        h1, title, description, status_code = get_seo_data(url_name)
        add_new_check(id, h1, title, description, status_code)
        flash('Страница успешно проверена', 'alert-success')
    except request_error:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('get_url', id=id))


@app.errorhandler(404)
def not_found(error):
    return render_template('error404.html'), 404


@app.errorhandler(500)
def parsing_error(error):
    return render_template('error500.html'), 500
