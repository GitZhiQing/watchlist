# 视图函数，是处理用户请求的函数，它们被 Flask 的路由装饰器关联到特定的 URL。

"""导入所需的库和模块
这包括 Flask 的 render_template（用于渲染模板），request（用于处理请求数据），url_for（用于生成 URL），redirect（用于重定向），flash（用于显示一次性消息），以及 flask_login 的 login_user，login_required，logout_user，current_user（用于处理用户会话）。还导入了 watchlist.app 和 watchlist.db（Flask 应用的实例和 SQLAlchemy 实例），以及 watchlist.models.User 和 Movie（用户和电影模型）。
"""

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie


# 主页视图函数
@app.route("/", methods=["GET", "POST"])
def index():
    # 如果是 POST 请求，那么获取表单数据并验证
    if request.method == "POST":
        # 如果当前用户未认证，那么重定向到主页
        if not current_user.is_authenticated:
            return redirect(url_for("index"))

        title = request.form["title"]
        year = request.form["year"]
        # 验证数据：电影标题不能为空，年份为四位数字
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for("index"))
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        # 显示成功创建的提示并重定向到主页
        flash("Item created.")
        return redirect(url_for("index"))
    # 读取所有电影记录并传递给模板
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


# 电影条目编辑视图函数
@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required  # 登录保护，未登录用户会被重定向到登录页面（设置了 login_manager.login_view = 'login'）
def edit(movie_id):
    # 根据传入的 movie_id 获取电影记录
    movie = Movie.query.get_or_404(movie_id)
    # 处理 POST 请求
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        # 验证数据：电影标题不能为空，年份为四位数字
        if not title or not year or len(year) != 4 or len(title) > 60:
            # 显示错误提示并重定向到编辑页面
            flash("Invalid input.")
            return redirect(url_for("edit", movie_id=movie_id))
        # 保存表单数据到数据库
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("Item updated.")
        return redirect(url_for("index"))
    # 传入被编辑的电影记录到编辑模板页面
    return render_template("edit.html", movie=movie)


# 电影条目删除视图函数
@app.route("/movie/delete/<int:movie_id>", methods=["POST"])
@login_required  # 登录保护
def delete(movie_id):
    # 根据主键查询对应的记录，如果找不到返回 404 错误
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted.")
    return redirect(url_for("index"))


# 更新用户 name 页面 
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form["name"]

        if not name or len(name) > 20:
            flash("Invalid input.")
            return redirect(url_for("settings"))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for("index"))

    return render_template("settings.html")


# 登录页面视图函数
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Invalid input.")
            return redirect(url_for("login"))

        # 验证用户名和密码是否一致
        user = User.query.first()
        # 验证成功，登录用户并跳转到主页
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("Login success.")
            return redirect(url_for("index"))
        # 验证失败，显示错误信息并重定向回登录页面
        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


# 登出页面视图函数
@app.route("/logout")
@login_required
def logout():
    logout_user() # 登出用户
    flash("Goodbye.")
    return redirect(url_for("index"))
