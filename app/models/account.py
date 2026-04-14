from .db import get_db_connection

class Account:
    """帳戶資料模型，處理 accounts 資料表的操作。"""

    @staticmethod
    def create(user_id, name, account_type, balance=0.0):
        """新增一個帳戶。"""
        try:
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
        except Exception as e:
            print(f"Error creating account: {e}")
            return None

    @staticmethod
    def get_all(user_id):
        """取得某位使用者的所有帳戶。"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []

    @staticmethod
    def get_by_id(account_id):
        """取得單一帳戶詳細資料。"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting account by id: {e}")
            return None

    @staticmethod
    def update(account_id, name, account_type, balance):
        """更新單一帳戶資料。"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE accounts SET name = ?, type = ?, balance = ? WHERE id = ?",
                (name, account_type, balance, account_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating account: {e}")
            return False

    @staticmethod
    def delete(account_id):
        """刪除單一帳戶。"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting account: {e}")
            return False
