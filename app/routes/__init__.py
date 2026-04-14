from flask import Flask

def register_routes(app: Flask):
    """
    註冊所有的 Blueprint 路由群組。
    """
    from .auth import bp as auth_bp
    from .main import bp as main_bp
    from .transactions import bp as transactions_bp
    from .settings import bp as settings_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(settings_bp, url_prefix='/settings')
