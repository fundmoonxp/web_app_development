import os
from flask import Flask
from dotenv import load_dotenv

# 嘗試載入環境變數
load_dotenv()

# 初始化 Flask 應用程式
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-fallback')

# 註冊所有 Blueprint 路由
from app.routes import register_routes
register_routes(app)

# 初始化資料庫
from app.models.db import init_db

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
