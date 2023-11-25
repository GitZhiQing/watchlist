# 模型类，定义了两个 SQLAlchemy 模型：User 和 Movie。这些模型用于创建和操作数据库表。

"""导入所需的库和模块
这包括 flask_login.UserMixin（用于处理用户会话），werkzeug.security.generate_password_hash 和 check_password_hash（用于处理密码哈希），以及 watchlist.db（Flask 应用的 SQLAlchemy 实例）。
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db

"""定义 User 模型类
继承自 db.Model 和 UserMixin。db.Model 用于表示数据库模型，UserMixin 为用户会话管理添加了必要的方法，比如 is_authenticated、is_active、is_anonymous 和 get_id。。这个模型有四个属性：id（主键，自动递增的整数），name（长度为 20 的字符串），username（长度为 20 的字符串），password_hash（长度为 128 的字符串）。这个模型还定义了两个方法：set_password（用于设置密码哈希）和 validate_password（用于验证密码）。
"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    # 用于设置密码哈希
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 用于验证密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


"""定义 Movie 模型类
继承自 db.Model。这个模型有三个属性：id（主键，自动递增的整数），title（长度为 60 的字符串），year（长度为 4 的字符串）。
"""


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
