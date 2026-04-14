from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('transactions', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    顯示歷史交易明細。
    處理邏輯：取得該帳號所有 TransactionLog 並遞減排序，傳入畫面。
    渲染：transactions/index.html (包含新增用的快速記帳表單)
    """
    pass

@bp.route('/', methods=['POST'])
def create():
    """
    建立新的交易明細。
    處理邏輯：接收 POST 參數，呼叫 TransactionLog.create()。同時檢查預算是否超支。
    輸出：成功與否的 flash 訊息，並 redirect 到 /transactions/ 繼續留在清單。
    """
    pass

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯既有交易。
    GET: 顯示附帶原有資料的表單 (transactions/edit.html)。
    POST: 修改現有資料庫欄位並重新運算差額至帳戶表。成功後 redirect 至列表。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除交易。
    處理邏輯：驗證權限後，將紀錄與關聯從資料庫抹除。
    輸出：重新導向回 /transactions/。
    """
    pass
