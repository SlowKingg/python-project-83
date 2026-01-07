import psycopg2
from psycopg2.extras import NamedTupleCursor


class DbContextManager:
    def __init__(self, db_url):
        self.db_url = db_url

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor(cursor_factory=NamedTupleCursor)
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def add_url(self, url):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,)
            )
            row = cursor.fetchone()
            return row.id if row else None  # pyright: ignore[reportAttributeAccessIssue]

    def get_url_by_id(self, url_id):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            row = cursor.fetchone()
            return row

    def get_url_by_name(self, url_name):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute("SELECT * FROM urls WHERE name = %s", (url_name,))
            row = cursor.fetchone()
            return row

    def get_all_urls(self):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute(
                """SELECT DISTINCT ON (urls.id)
                        urls.id,
                        urls.name,
                        url_checks.status_code,
                        url_checks.created_at AS last_check_at
                        FROM urls
                        LEFT JOIN url_checks
                        ON urls.id = url_checks.url_id
                        ORDER BY urls.id DESC
                    """
            )
            rows = cursor.fetchall()
            return rows

    def add_url_check(self, url_id, status_code, h1, title, description):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute(
                """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (url_id, status_code, h1, title, description),
            )

    def get_url_checks(self, url_id):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute(
                """
                    SELECT * FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC
                    """,
                (url_id,),
            )
            rows = cursor.fetchall()
            return rows

    def get_last_url_check(self, url_id):
        with DbContextManager(self.db_url) as (conn, cursor):
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
            return row

    def get_url_check_by_id(self, check_id):
        with DbContextManager(self.db_url) as (conn, cursor):
            cursor.execute(
                "SELECT * FROM url_checks WHERE id = %s", (check_id,)
            )
            row = cursor.fetchone()
            return row
