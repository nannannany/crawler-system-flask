import os

from flask import Flask, render_template
from .routes import register_routes
from config.db import db, DB_URI


def create_app():
    # 获取项目根目录
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # 指定静态文件和模板路径
    app = Flask(
        __name__,
        static_folder=os.path.join(base_dir, 'www', 'assets'),  # assets 目录
        static_url_path='/assets',  # 静态文件 URL 前缀
        template_folder=os.path.join(base_dir, 'www')  # index.html 所在位置
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    register_routes(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue(path):
        # 检查 assets 目录
        static_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(static_path):
            return app.send_static_file(path)

        # 检查模板目录（index.html、favicon.ico等）
        template_path = os.path.join(app.template_folder, path)
        if path and os.path.exists(template_path):
            return app.send_static_file(path)

        # 默认返回前端入口文件
        return render_template('index.html')

    return app
