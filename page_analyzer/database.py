from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, db_connection):
        self.conn = db_connection

    def add_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row["id"]

    def get_url_by_id(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_url_by_name(self, url_name):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (url_name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_urls(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def add_url_check_dummy(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (url_id, 200, "Dummy H1", "Dummy Title", "Dummy Description"),
            )
            self.conn.commit()

    def add_url_check(self, url_id, status_code, h1, title, description):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (url_id, status_code, h1, title, description),
            )
            self.conn.commit()

    def get_url_checks(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC",
                (url_id,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_last_url_check(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
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
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM url_checks WHERE id = %s", (check_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
