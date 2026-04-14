from .db import get_db_connection

class TransactionLog:
    """收支明細資料模型，處理 transaction_log 資料表的操作。"""

    @staticmethod
    def create(user_id, account_id, category_id, amount, t_type, date, note):
        """建立新的記帳明細並更新對應帳戶的餘額。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO transaction_log (user_id, account_id, category_id, amount, type, transaction_date, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, account_id, category_id, amount, t_type, date, note)
            )
            balance_change = amount if t_type == 'income' else -amount
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (balance_change, account_id)
            )
            conn.commit()
            t_id = cursor.lastrowid
            conn.close()
            return t_id
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None

    @staticmethod
    def get_all(user_id):
        """取得某位使用者的所有記帳明細。"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM transaction_log WHERE user_id = ? ORDER BY transaction_date DESC", (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    @staticmethod
    def get_by_id(t_id):
        """取得單一筆記帳資料。"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT * FROM transaction_log WHERE id = ?", (t_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting transaction by id: {e}")
            return None

    @staticmethod
    def update(t_id, account_id, category_id, amount, t_type, date, note):
        """更新單筆明細，並還原舊帳戶餘額、套用新帳戶餘額。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            old_t = cursor.execute("SELECT * FROM transaction_log WHERE id = ?", (t_id,)).fetchone()
            if not old_t:
                return False
            
            # 還原舊餘額
            old_change = -old_t['amount'] if old_t['type'] == 'income' else old_t['amount']
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (old_change, old_t['account_id']))
            
            # 套用新餘額
            new_change = amount if t_type == 'income' else -amount
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (new_change, account_id))
            
            # 更新本體
            cursor.execute(
                """
                UPDATE transaction_log 
                SET account_id = ?, category_id = ?, amount = ?, type = ?, transaction_date = ?, note = ?
                WHERE id = ?
                """,
                (account_id, category_id, amount, t_type, date, note, t_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False

    @staticmethod
    def delete(t_id):
        """刪除單筆明細並回復帳戶餘額。"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            t = cursor.execute("SELECT * FROM transaction_log WHERE id = ?", (t_id,)).fetchone()
            if t:
                balance_restore = -t['amount'] if t['type'] == 'income' else t['amount']
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (balance_restore, t['account_id']))
                cursor.execute("DELETE FROM transaction_log WHERE id = ?", (t_id,))
                conn.commit()
                conn.close()
                return True
            conn.close()
            return False
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
