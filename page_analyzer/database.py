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
