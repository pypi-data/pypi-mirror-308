import json

try:
    import psycopg2
    from psycopg2.extras import execute_values
    from pgvector.psycopg2 import register_vector
except ImportError as e:
    print(e)
    print("psycopg2 library not found. Please install it using 'pip install psycopg2'")
    print("pgvector library not found. Please install it using 'pip install pgvector'")
    exit()

from ...core import BaseVectorDB, BaseVectorizer


class PgVectorVDBMixin(BaseVectorDB):
    def __init__(self, vectorizer: BaseVectorizer, dbname: str, user: str, password: str, host: str = "localhost",
                 port: str = "5432"):
        super().__init__(vectorizer)
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        register_vector(self.conn)
        self._setup_table()

    def _setup_table(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS chunks (
                uuid TEXT PRIMARY KEY,
                text TEXT,
                embedding VECTOR({self.vectorizer.dimensions}),
                meta JSONB
                )
            """)
            self.conn.commit()

    def insert(self, uuid: str, text: str, meta: dict) -> None:
        embedding = self.vectorizer.vectorize(text)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chunks (uuid, text, embedding, meta)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (uuid) DO NOTHING
            """, (uuid, text, embedding, json.dumps(meta)))
            self.conn.commit()

    def bulk_insert(self, data: list[dict]) -> None:
        data = [d for d in data if d['text']]
        documents = [(d['uuid'], d['text'], self.vectorizer.vectorize(d['text']), json.dumps(d['meta'])) for d in data]
        with self.conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO chunks (uuid, text, embedding, meta)
                VALUES %s
                ON CONFLICT (uuid) DO NOTHING
            """, documents)
            self.conn.commit()

    def query(self, query: list[float], num_results: int, where: dict | None = None) -> list[dict]:
        vector_query_str = ','.join(map(str, query))
        #  TODO add where clause

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT uuid, text
                FROM chunks
                ORDER BY embedding <=> vector('[{vector_query_str}]')
                LIMIT %s
            """, (num_results,))

            results = cur.fetchall()

        response = [{'uuid': uuid, 'text': text} for uuid, text in results]
        return response


class PgVectorVDB(PgVectorVDBMixin):
    def __init__(self, vectorizer: BaseVectorizer, dbname: str, user: str, password: str, host: str = "localhost",
                 port: str = "5432"):
        super().__init__(vectorizer, dbname, user, password, host, port)
