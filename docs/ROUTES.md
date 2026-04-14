# API 路由與頁面設計文件

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 使用者註冊 | GET / POST | `/auth/register` | `auth/register.html` | 顯示或送出註冊表單 |
| 使用者登入 | GET / POST | `/auth/login` | `auth/login.html` | 顯示或送出登入表單 |
| 使用者登出 | POST | `/auth/logout` | — | 清除 Session 並導向登入頁 |
| 儀表板(首頁) | GET | `/` | `dashboard.html` | 呈現報表、預算與帳戶餘額 |
| 明細列表 | GET | `/transactions/` | `transactions/index.html` | 條列歷史收支明細，含新增表單 |
| 新增明細 | POST | `/transactions/` | — | 接收寫入 DB 並重新導回列表 |
| 編輯明細 | GET / POST | `/transactions/<id>/edit` | `transactions/edit.html` | 呈現特定明細編輯視窗/送出修改 |
| 刪除明細 | POST | `/transactions/<id>/delete`| — | 執行刪除並重新導向 |
| 設定頁首頁 | GET | `/settings/` | `settings/index.html` | 呈現分類、帳戶與預算設定 |
| 新增帳戶 | POST | `/settings/accounts` | — | 接收並新增用戶資金帳戶 |
| 新增/更新分類| POST | `/settings/categories` | — | 自定義消費或收入分類 |
| 設定預算 | POST | `/settings/budgets` | — | 寫入或更新當月預算目標 |

## 2. 每個路由的詳細說明

### 2.1 修改與新增明細 (`/transactions/`)
- **輸入**: 從 `POST` 接收 `account_id`, `category_id`, `amount`, `type`, `date`, `note` 表單欄位。
- **處理邏輯**: 取出 Session 中的 `user_id`，呼叫 `Transaction.create()`。完成後呼叫 `Budget.get_by_month()` 檢查是否透支。
- **輸出**: 配合 `flash()` 將超支警告或建立成功訊息暫存，隨後 `redirect(url_for('transactions.index'))`。
- **錯誤處理**: 若有漏填必填欄位，回傳 flash 錯誤並重新導回列表頁。若是無權限的 ID，於 `<id>/edit` 中回傳 404 或 403。

### 2.2 儀表板 (`/`)
- **輸入**: GET 要求（無額外參數）。
- **處理邏輯**: 驗證登入狀態。利用 `Transaction.get_all_by_user()` 搭配時間過濾，取得按分類加總的金額，整理為 JSON；以及將 `Account.get_by_user()` 資料取回。
- **輸出**: 渲染 `dashboard.html`，將 JSON 資料打包給前端 Chart.js 處理。

### 2.3 刪除操作 (`/transactions/<id>/delete`)
- **輸入**: 表單發出 POST 請求。
- **處理邏輯**: 驗證該筆名細是否為當前用戶建立。驗證過後呼叫 `Transaction.delete(id)`，並自動由 Model 調校回帳戶餘額。
- **輸出**: 重導向至明細列表。

## 3. Jinja2 模板清單

所有的視圖模板會以 Jinja2 的繼承（繼承自 `base.html`）撰寫，維持一致的佈局與選單。這份清單供前端實作時參考：
- `base.html`：整體外部框架，含導覽列 (Navbar)、Meta 標籤、載入 CSS/JS 與 Flash 訊息顯示區。
- `auth/login.html`：登入畫面。繼承 `base.html`，可能隱藏導覽列。
- `auth/register.html`：註冊畫面。
- `dashboard.html`：主要儀表板。加入 Canvas 圖表區塊與預算顏色進度條。
- `transactions/index.html`：左側為過往清單，右側或上側提供「快速記帳表單」。
- `transactions/edit.html`：為單一明細的修改介面。
- `settings/index.html`：提供數個頁籤或卡片區塊，分別用以新增/修改帳戶清單、分類標籤、以及整體預算上限額度。

## 4. 路由骨架程式碼
對應的 Python Model 與 Blueprint 設計已經準備完畢，存放於 `app/routes/` 之中。
