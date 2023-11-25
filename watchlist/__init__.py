# 包构造文件，创建程序实例，初始化扩展的代码放到包构造文件里（__init__.py）

import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI 前缀
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


"""实例化 Flask 类创建程序实例
创建一个 Flask 应用实例，并设置一些配置项。这包括 SECRET_KEY（用于保护会话和 cookie），SQLALCHEMY_DATABASE_URI（数据库的 URI），SQLALCHEMY_TRACK_MODIFICATIONS（是否追踪对象的修改，以触发信号）。
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(
    os.path.dirname(app.root_path), os.getenv("DATABASE_FILE", "data.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 实例化扩展类
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# 用户加载回调函数，接受用户 ID 作为参数，返回用户对象到变量 current_user
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User

    user = User.query.get(int(user_id))
    return user


login_manager.login_view = "login"
# login_manager.login_message = 'Your custom message'


# 模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User

    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
