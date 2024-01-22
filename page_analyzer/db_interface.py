from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def make_connection():
    return psycopg2.connect(DATABASE_URL)


def exec_query(query, with_data_return=True):
    with make_connection() as conn:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query)
        if with_data_return:
            data = cursor.fetchall()
        cursor.close()
    return data if with_data_return else None


def get_all_urls():
    return exec_query("""SELECT
        urls.id, urls.name,
        url_checks.status_code,
        url_checks.created_at
        FROM urls LEFT JOIN url_checks
        ON urls.id = url_checks.url_id
        AND url_checks.created_at = (SELECT
        MAX(created_at) FROM url_checks
        WHERE url_id = urls.id)
        ORDER BY urls.id;
    """)
