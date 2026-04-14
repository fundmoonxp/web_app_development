from .db import get_db_connection

class User:
    """使用者資料模型，處理 users 資料表的 CRUD 操作。"""

    @staticmethod
    def create(username, password_hash):
        """建立新使用者。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得單一使用者。"""
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者（系統管理用）。"""
        try:
            conn = get_db_connection()
            users = conn.execute("SELECT * FROM users").fetchall()
            conn.close()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def update(user_id, password_hash):
        """更新使用者資料（例如密碼）。"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除指定使用者。"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    @staticmethod
    def get_by_username(username):
        """根據 username 取得單一使用者（登入用）。"""
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
