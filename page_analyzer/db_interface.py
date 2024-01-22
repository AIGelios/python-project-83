from datetime import datetime
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2.errors import UniqueViolation


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def make_connection():
    return psycopg2.connect(DATABASE_URL)


def exec_query(query, fetch_data=True):
    with make_connection() as conn:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query)
        data = cursor.fetchall() if fetch_data else None
        cursor.close()
    return data


url_already_exists_error = UniqueViolation


def get_all_urls():
    query = """
        SELECT urls.id, urls.name,
        url_checks.status_code,
        url_checks.created_at
        FROM urls LEFT JOIN url_checks
        ON urls.id = url_checks.url_id
        AND url_checks.created_at = (SELECT
        MAX(created_at) FROM url_checks
        WHERE url_id = urls.id)
        ORDER BY urls.id;
    """
    return exec_query(query)


def add_new_url(url_name):
    query = f"""
        INSERT INTO urls (name, created_at)
        VALUES ('{url_name}', '{datetime.now()}');
    """
    exec_query(query, fetch_data=False)


def get_url_id_by_name(url_name):
    query = f"""
        SELECT id FROM urls
        WHERE name = '{url_name}';
    """
    return exec_query(query)[0].id


def get_url_by_id(id):
    query = f"""
        SELECT * FROM urls
        WHERE id = {id};
    """
    matched = exec_query(query)
    return matched[0] if matched else None


def get_checks_by_url_id(id):
    query = f"""
        SELECT * FROM url_checks
        WHERE url_id = {id}
        ORDER BY id DESC;
    """
    return exec_query(query)


def get_url_name_by_id(url_id):
    url = get_url_by_id(url_id)
    return url.name if url else ''


def add_new_check(id, h1, title, description, status_code):
    query = f"""
        INSERT INTO url_checks (
        url_id, h1, title, description, status_code, created_at)
        VALUES (
        {id}, '{h1}', '{title}', '{description}', {status_code},
        '{datetime.now()}');
    """
    exec_query(query, fetch_data=False)
