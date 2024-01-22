from .db_connections import exec_query
from datetime import datetime


# ---------------------------------------------------------
def get_all_urls():
    query = """SELECT
        urls.id, urls.name,
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


# ---------------------------------------------------------
def add_new_url(url_name):
    query = f"""
        INSERT INTO urls (name, created_at)
        VALUES ('{url_name}', '{datetime.now()}');
    """
    exec_query(query, fetch_data=False)


# ---------------------------------------------------------
def get_url_id_by_name(url_name):
    query = f"SELECT id FROM urls WHERE name = '{url_name}';"
    return exec_query(query)[0].id


# ---------------------------------------------------------
def get_url_data_by_id_query(id):
    return f"SELECT * FROM urls WHERE id = {id}"


# ---------------------------------------------------------
def add_check_query(id, h1, title, description, status_code):
    return f"""
        INSERT INTO url_checks (
        url_id, h1, title, description, status_code, created_at)
        VALUES (
        {id}, '{h1}', '{title}', '{description}', {status_code},
        '{datetime.now()}');
    """


def get_url_by_id_query(id):
    return f"SELECT name FROM urls WHERE id = {id};"


def get_checks_by_url_id(id):
    return f"""SELECT * FROM url_checks WHERE url_id = {id}
    ORDER BY id DESC;"""
