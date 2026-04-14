from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('settings', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    顯示所有設定項目。
    處理邏輯：取得所有 Category、Account 與 Budget 提供前端渲染卡片。
    渲染：settings/index.html
    """
    pass

@bp.route('/categories', methods=['POST'])
def create_category():
    """新增自定義收支分類，並重新導向回 /settings/。"""
    pass

@bp.route('/accounts', methods=['POST'])
def create_account():
    """新增使用者資金銀行帳戶或卡片，並重新導向回 /settings/。"""
    pass

@bp.route('/budgets', methods=['POST'])
def update_budget():
    """設定與更新特定分類或總金額在指定月份的預算，並重新導向回 /settings/。"""
    pass
