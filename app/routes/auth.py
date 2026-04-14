from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染登入表單 auth/login.html。
    POST: 接收 username 與 password 進行驗證。若成功則寫入 Session 並導向首頁；失敗則 flash 錯誤。
    """
    pass

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染註冊表單 auth/register.html。
    POST: 驗證表單並建立新使用者，完成後導向登入頁面。
    """
    pass

@bp.route('/logout', methods=['POST'])
def logout():
    """
    處理登出。
    清除使用者的 Session 資訊並重新導向至登入頁面。
    """
    pass
