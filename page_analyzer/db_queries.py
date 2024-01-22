from .service_module import get_current_timestamp
from .db_connections import exec_query


def get_all_urls_query():
    return """SELECT
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


def get_all_urls():
    query = get_all_urls_query()
    return exec_query(query)


def add_url_query(url):
    return f"""
    INSERT INTO urls (name, created_at)
    VALUES ('{url}', '{get_current_timestamp()}');
    """


def get_id_by_url_query(name):
    return f"SELECT id FROM urls WHERE name = '{name}';"


def get_url_data_by_id_query(id):
    return f"SELECT * FROM urls WHERE id = {id}"


def add_check_query(id, h1, title, description, status_code):
    return f"""
        INSERT INTO url_checks (
        url_id, h1, title, description, status_code, created_at)
        VALUES (
        {id}, '{h1}', '{title}', '{description}', {status_code},
        '{get_current_timestamp()}');
    """


def get_url_by_id_query(id):
    return f"SELECT name FROM urls WHERE id = {id};"


def get_checks_by_url_id(id):
    return f"""SELECT * FROM url_checks WHERE url_id = {id}
    ORDER BY id DESC;"""
