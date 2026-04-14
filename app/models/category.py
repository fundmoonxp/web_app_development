from .db import get_db_connection

class Category:
    """分類資料模型，處理 categories 資料表的操作。"""

    @staticmethod
    def create(user_id, name, c_type):
        """新增一個分類。"""
        try:
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
        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    @staticmethod
    def get_all(user_id):
        """取得系統預設(user_id IS NULL)以及特定使用者的分類。"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM categories WHERE user_id IS NULL OR user_id = ?", 
                (user_id,)
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    @staticmethod
    def get_by_id(cat_id):
        """取得單一分類。"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT * FROM categories WHERE id = ?", (cat_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting category by id: {e}")
            return None

    @staticmethod
    def update(cat_id, name, c_type):
        """更新自定義分類。"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE categories SET name = ?, type = ? WHERE id = ?",
                (name, c_type, cat_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    @staticmethod
    def delete(cat_id):
        """刪除單一自定義分類。"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
