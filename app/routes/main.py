from flask import Blueprint, render_template, g, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    """
    顯示總覽儀表板。
    如果使用者未登入，重導向至登入頁。
    處理邏輯：
    1. 取得使用者的各個帳戶最新餘額。
    2. 從資料庫取得該月份按「分類」加總的花費，供前端圖表繪製。
    3. 取得本月預算狀態判斷是否超過。
    渲染：dashboard.html
    """
    pass
