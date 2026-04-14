# 流程圖文件：簡易記帳系統

這份文件根據 PRD 需求與系統架構，將使用者的操作動線與系統資料流視覺化，以便團隊在開發前對整體流程有明確的共識。

---

## 1. 使用者流程圖 (User Flow)

此流程圖從使用者進入網站的首頁（儀表板）開始，涵蓋了查看圖表、新增記帳、以及進行相關設定的路徑。

```mermaid
flowchart TD
    Start([使用者開啟網頁]) --> Dashboard[首頁 - 儀表板 Dashboard]
    
    Dashboard --> ActionChoice{要執行什麼操作？}
    
    ActionChoice -->|看圖表分析| ViewChart[檢視消費圓餅圖與餘額]
    ActionChoice -->|看歷史明細| ViewTx[進入收支紀錄列表]
    ActionChoice -->|記一筆帳| QuickAdd[點擊「快速記帳」按鈕]
    ActionChoice -->|調整設定| Settings[進入系統設定頁面]
    
    %% 記帳流程
    QuickAdd --> FillForm[填寫表單：金額、分類、帳戶、日期]
    FillForm --> SubmitTx{確定送出？}
    SubmitTx -->|是| CheckBudget{是否超過預算上限？}
    CheckBudget -->|是| Alert[系統顯示超支警告提示] --> BackToDash[回到儀表板或列表頁]
    CheckBudget -->|否| SuccessMsg[顯示新增成功] --> BackToDash
    SubmitTx -->|取消| CancelAdd[放棄新增] --> BackToDash
    
    %% 明細操作
    ViewTx --> ModifyTxChoice{是否操作單筆明細？}
    ModifyTxChoice -->|編輯| EditTx[修改金額或分類] --> SubmitTx
    ModifyTxChoice -->|刪除| DeleteTx[確認刪除] --> BackToDash
    
    %% 設定流程
    Settings --> SetBudget[設定每月預算上限]
    Settings --> SetCategory[新增/修改自定義分類]
    Settings --> SetFixed[設定固定支出自動帶入]
```

---

## 2. 系統序列圖 (Sequence Diagram)

此序列圖展示了核心功能**「新增一筆記帳並檢查預算」**的系統底層運作流程，涵蓋了前端瀏覽器、後端 Flask 控制器以及 SQLite 資料庫的互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask Route (Controller)
    participant Model as Database Model (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫記帳表單並點擊「送出」
    Browser->>Flask: POST /transactions (夾帶輸入的表單資料)
    
    %% 寫入資料
    Flask->>Model: 呼叫明細建立方法 (如 Transaction.create)
    Model->>DB: 執行 SQL: INSERT INTO transactions ...
    DB-->>Model: 寫入成功，回傳新資料 ID
    Model-->>Flask: 回報建立成功
    
    %% 檢查預算邏輯
    Flask->>Model: 查詢當月特定分類或總花費加總
    Model->>DB: 執行 SQL: SELECT SUM(amount) ...
    DB-->>Model: 回傳加總數字
    Model-->>Flask: 取得月總額
    
    %% 判斷並回傳結果
    alt 總額 >= 設定的預算上限
        Flask->>Browser: HTTP 302 重導向並發送「預算超支」Flash 警告訊息
    else 尚在預算內
        Flask->>Browser: HTTP 302 重導向並發送「記帳成功」Flash 提示訊息
    end
    
    Browser->>User: 重新渲染畫面，使用者看到最新餘額與提示字眼
```

---

## 3. 功能清單對照表

下表列出系統主要功能所對應的入口 URL 路徑與 HTTP 方法，為接下來的 API/Routing 設計提供初步指引。

| 功能區塊 | 操作描述 | 建議的 URL 路徑 | HTTP 方法 |
| --- | --- | --- | --- |
| **首頁儀表板** | 顯示消費圖表、各帳戶餘額、預算進度 | `/` 或 `/dashboard` | GET |
| **收支明細** | 列表顯示歷史記帳資料 | `/transactions` | GET |
| **快速記帳** | 送出新增明細的表單 | `/transactions` | POST |
| **編輯明細** | 進入編輯明細表單畫面 | `/transactions/<id>/edit` | GET |
| **更新明細** | 送出更新後的明細資料 | `/transactions/<id>/edit` | POST |
| **刪除明細** | 將該明細從資料庫刪除 | `/transactions/<id>/delete` | POST |
| **系統設定** | 頁面呈現：管理預算、分類、固定開銷 | `/settings` | GET |
| **更新設定** | 儲存更改的設定項目 (新增分類等) | `/settings/update` | POST |
