from .db import get_db_connection

class TransactionLog:
    @staticmethod
    def create(user_id, account_id, category_id, amount, t_type, date, note):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transaction_log (user_id, account_id, category_id, amount, type, transaction_date, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, account_id, category_id, amount, t_type, date, note)
        )
        # Simultaneously update account balance
        balance_change = amount if t_type == 'income' else -amount
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (balance_change, account_id)
        )
        conn.commit()
        t_id = cursor.lastrowid
        conn.close()
        return t_id

    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM transaction_log WHERE user_id = ? ORDER BY transaction_date DESC", (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def delete(t_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 先取得這筆明細以還原帳戶餘額
        t = cursor.execute("SELECT * FROM transaction_log WHERE id = ?", (t_id,)).fetchone()
        if t:
            balance_restore = -t['amount'] if t['type'] == 'income' else t['amount']
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (balance_restore, t['account_id']))
            cursor.execute("DELETE FROM transaction_log WHERE id = ?", (t_id,))
            conn.commit()
            success = True
        else:
            success = False
            
        conn.close()
        return success
