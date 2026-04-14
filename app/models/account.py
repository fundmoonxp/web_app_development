from .db import get_db_connection

class Account:
    @staticmethod
    def create(user_id, name, account_type, balance=0.0):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (user_id, name, type, balance) VALUES (?, ?, ?, ?)",
            (user_id, name, account_type, balance)
        )
        conn.commit()
        acc_id = cursor.lastrowid
        conn.close()
        return acc_id

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
