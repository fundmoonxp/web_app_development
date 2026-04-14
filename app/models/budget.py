from .db import get_db_connection

class Budget:
    @staticmethod
    def create(user_id, category_id, amount, month_str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO budgets (user_id, category_id, amount, month_str)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, category_id, amount, month_str)
        )
        conn.commit()
        budget_id = cursor.lastrowid
        conn.close()
        return budget_id

    @staticmethod
    def get_by_month(user_id, month_str):
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM budgets WHERE user_id = ? AND month_str = ?",
            (user_id, month_str)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
