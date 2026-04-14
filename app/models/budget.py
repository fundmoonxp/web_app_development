from .db import get_db_connection

class Budget:
    """預算資料模型，處理 budgets 資料表的操作。"""

    @staticmethod
    def create(user_id, category_id, amount, month_str):
        """新增一筆預算設定。"""
        try:
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
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None

    @staticmethod
    def get_all(user_id):
        """取得該用戶所有預算。"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM budgets WHERE user_id = ?", (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []

    @staticmethod
    def get_by_id(budget_id):
        """取得單一筆預算設定。"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT * FROM budgets WHERE id = ?", (budget_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting budget by id: {e}")
            return None

    @staticmethod
    def update(budget_id, category_id, amount, month_str):
        """更新預算設定。"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE budgets SET category_id = ?, amount = ?, month_str = ? WHERE id = ?",
                (category_id, amount, month_str, budget_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating budget: {e}")
            return False

    @staticmethod
    def delete(budget_id):
        """刪除單筆預算。"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting budget: {e}")
            return False

    @staticmethod
    def get_by_month(user_id, month_str):
        """取得該用戶指定年月的預算。"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM budgets WHERE user_id = ? AND month_str = ?",
                (user_id, month_str)
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error getting budgets by month: {e}")
            return []
