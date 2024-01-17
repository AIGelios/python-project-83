from .service_module import get_current_timestamp


def get_urls_query():
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


def insert_url_query(url):
    return f"""
    INSERT INTO urls (name, created_at)
    VALUES ('{url}', '{get_current_timestamp()}');
    """


def get_url_id_query(url):
    return f"SELECT id FROM urls WHERE name = '{url}';"
