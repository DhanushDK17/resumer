import psycopg2
from psycopg2 import sql
from settings import settings

def get_db_connection():
    conn = psycopg2.connect(settings.database_url)
    return conn

def create_resumes_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id SERIAL PRIMARY KEY,
            job_url TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_resume(job_url: str, file_path: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resumes (job_url, file_path) VALUES (%s, %s)",
        (job_url, file_path)
    )
    conn.commit()
    cur.close()
    conn.close()
