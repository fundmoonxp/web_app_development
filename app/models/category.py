from .db import get_db_connection

class Category:
    @staticmethod
    def create(user_id, name, c_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)",
            (user_id, name, c_type)
        )
        conn.commit()
        cat_id = cursor.lastrowid
        conn.close()
        return cat_id

    @staticmethod
    def get_all(user_id):
        # 取得系統預設(user_id IS NULL)以及該使用者的分類
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM categories WHERE user_id IS NULL OR user_id = ?", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
