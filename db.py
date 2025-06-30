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
            password TEXT NOT NULL
        );
    """)
def create_task_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            owner_email TEXT REFERENCES users(email) ON DELETE CASCADE,
            title TEXT NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT FALSE
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
def get_tasks(owner_email: str):
    cur.execute(
        "SELECT id, title, is_completed FROM tasks WHERE owner_email = %s;",
        (owner_email,)
    )
    return cur.fetchall()
def update_task(task_id: int, title: str, is_completed: bool):
    cur.execute(
        "UPDATE tasks SET title = %s, is_completed = %s WHERE id = %s;",
        (title, is_completed, task_id)
    )

def get_task_owner(task_id: int):
    cur.execute(
        "SELECT owner_email FROM tasks WHERE id = %s;",
        (task_id,)
    )
    result = cur.fetchone()
    return result[0] if result else None

def get_password_hash(email: str):
    cur.execute(
        "SELECT password FROM users WHERE email = %s;",
        (email,)
    )
    result = cur.fetchone()
    return result[0] if result else None
