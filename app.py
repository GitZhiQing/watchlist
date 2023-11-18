# 从 flask 包导入 Flask 类
from flask import Flask, url_for, render_template
from markupsafe import escape

# 通过实例化 Flask 类创建对象 app
app = Flask(__name__)

name = "QING"
movies = [
    {"title": "My Neighbor Totoro", "year": "1988"},
    {"title": "Dead Poets Society", "year": "1989"},
    {"title": "A Perfect World", "year": "1993"},
    {"title": "Leon", "year": "1994"},
    {"title": "Mahjong", "year": "1996"},
    {"title": "Swallowtail Butterfly", "year": "1996"},
    {"title": "King of Comedy", "year": "1999"},
    {"title": "Devils on the Doorstep", "year": "1999"},
    {"title": "WALL-E", "year": "2008"},
    {"title": "The Pork of Music", "year": "2012"},
]


# 通过 app.route 装饰器来为这个函数绑定对应的 URL
@app.route("/")
def index():
    return render_template("index.html", name=name, movies=movies)


@app.route("/user/<name>")
def user_page(name):
    return f"Welcome user: {escape(name)}"


@app.route("/test")
def test_url_for():
    print(url_for("hello"))
    print(url_for("user_page", name="QING"))  # /user/QING
    print(url_for("user_page", name="CLEAR"))  # /user/CLEAR
    print(url_for("test_url_for"))
    print(url_for("test_url_for", num=1))
    return "Test Page"
