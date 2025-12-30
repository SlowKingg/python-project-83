import psycopg2
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def add_url(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,)
                )
                row = cursor.fetchone()
                conn.commit()
                return row["id"] if row else None

    def get_url_by_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
                row = cursor.fetchone()
                return dict(row) if row else None

    def get_url_by_name(self, url_name):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM urls WHERE name = %s", (url_name,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None

    def get_all_urls(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """SELECT urls.id, urls.name,
                       url_checks.status_code,
                       url_checks.created_at AS last_check_at
                       FROM urls
                       LEFT JOIN url_checks
                       ON urls.id = url_checks.url_id
                       ORDER BY urls.id DESC
                    """
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]

    def add_url_check(self, url_id, status_code, h1, title, description):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                    (url_id, status_code, h1, title, description),
                )
                conn.commit()

    def get_url_checks(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC
                    """,
                    (url_id,),
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]

    def get_last_url_check(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (url_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None

    def get_url_check_by_id(self, check_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM url_checks WHERE id = %s", (check_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
