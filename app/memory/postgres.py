import psycopg2
from app.config import (
    POSTGRES_HOST,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

def persist_execution(user_id: str, input_text: str, output_text: str):
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO agent_runs (user_id, input, output)
        VALUES (%s, %s, %s)
        """,
        (user_id, input_text, output_text)
    )
    conn.commit()
    cur.close()
    conn.close()
