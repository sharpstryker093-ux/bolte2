import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "site.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS service (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            sort_order INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contact_message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT
        )
    """)
    conn.commit()

    # Serviços de exemplo, se a tabela estiver vazia
    count = conn.execute("SELECT COUNT(*) FROM service").fetchone()[0]
    if count == 0:
        exemplos = [
            ("Branding", "Construção de identidade visual e posicionamento de marca.", 1),
            ("Marketing Digital", "Estratégias de tráfego, conteúdo e performance.", 2),
            ("Desenvolvimento Web", "Sites e sistemas sob medida para o seu negócio.", 3),
        ]
        conn.executemany(
            "INSERT INTO service (title, description, sort_order) VALUES (?, ?, ?)",
            exemplos,
        )
        conn.commit()
    conn.close()


# ---------- Usuários ----------

def create_user(name, email, password):
    conn = get_conn()
    try:
        total_usuarios = conn.execute("SELECT COUNT(*) FROM user").fetchone()[0]
        is_admin = 1 if total_usuarios == 0 else 0  # o primeiro cadastro vira admin
        conn.execute(
            "INSERT INTO user (name, email, password_hash, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, generate_password_hash(password), is_admin, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def verify_password(user_row, password):
    return check_password_hash(user_row["password_hash"], password)


# ---------- Serviços ----------

def list_services():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM service ORDER BY sort_order").fetchall()
    conn.close()
    return rows


def add_service(title, description):
    conn = get_conn()
    max_order = conn.execute("SELECT MAX(sort_order) FROM service").fetchone()[0] or 0
    conn.execute(
        "INSERT INTO service (title, description, sort_order) VALUES (?, ?, ?)",
        (title, description, max_order + 1),
    )
    conn.commit()
    conn.close()


def delete_service(service_id):
    conn = get_conn()
    conn.execute("DELETE FROM service WHERE id = ?", (service_id,))
    conn.commit()
    conn.close()


# ---------- Mensagens de contato ----------

def add_contact_message(name, email, message):
    conn = get_conn()
    conn.execute(
        "INSERT INTO contact_message (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def list_contact_messages():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM contact_message ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows
