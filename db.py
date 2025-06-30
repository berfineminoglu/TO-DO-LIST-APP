import psycopg2
from psycopg2 import sql

# 1) Veritabanına bağlan
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="to-do-list",
    user="postgres",
    password="admin"
)

# Otomatik commit için:
conn.autocommit = True

# 2) Cursor oluştur
cur = conn.cursor()

# 3) Fonksiyonlar
def create_user_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL,
        );
    """)
def create_task_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            owner_email TEXT REFERENCES users(email) ON DELETE CASCADE,
            title TEXT NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT FALSE,
        );
    """)
def insert_user(email: str, password: str):
    cur.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s);",
        (email, password)
    )
def insert_task(owner_email: str, title: str):
    cur.execute(
        "INSERT INTO tasks (owner_email, title) VALUES (%s, %s);",
        (owner_email, title)
    )
def delete_task(task_id: int):
    cur.execute(
        "DELETE FROM tasks WHERE id = %s;",
        (task_id,)
    )
def read_tasks(owner_email: str):
    cur.execute(
        "SELECT id, title, is_completed FROM tasks WHERE owner_email = %s;",
        (owner_email,)
    )
    return cur.fetchall()
def update_task(task_id: int, is_completed: bool):
    cur.execute(
        "UPDATE tasks SET is_completed = %s WHERE id = %s;",
        (is_completed, task_id)
    )

# 4) Kapatma (program sonunda)
cur.close()
conn.close()