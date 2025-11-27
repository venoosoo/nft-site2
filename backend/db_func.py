import sqlite3

DB_PATH = "gifts.db"


def get_random_row():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT collection, gift_id, price FROM gifts ORDER BY RANDOM() LIMIT 1;")
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def add_user_id_and_phone(user_id: int, phone_number: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO USERS (user_id, phone_number) VALUES (?, ?)",
            (user_id, phone_number)
        )

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("DB error:", e)
        return False


def get_num_from_id(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()

        cur.execute("SELECT phone_number FROM Users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()

        return dict(row) if row else None

    except Exception as e:
        print("DB error:", e)
        return False
