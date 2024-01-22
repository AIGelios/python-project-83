from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor


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
