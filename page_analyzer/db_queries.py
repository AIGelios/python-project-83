from .service_module import get_current_timestamp


def get_all_urls_query():
    return """SELECT
        id, name
        FROM urls
        ORDER BY urls.id;
    """


def insert_url_query(url):
    return f"""
    INSERT INTO urls (name, created_at)
    VALUES ('{url}', '{get_current_timestamp()}');
    """


def get_id_by_url_query(url):
    return f"SELECT id FROM urls WHERE name = '{url}';"


def get_url_data_by_id_query(id):
    return f"SELECT * FROM urls WHERE id = {id}"
