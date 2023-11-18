# 从 flask 包导入 Flask 类
from flask import Flask,url_for
from markupsafe import escape

# 通过实例化 Flask 类创建对象 app
app = Flask(__name__)

# 通过 app.route 装饰器来为这个函数绑定对应的 URL
@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return f'Welcome user: {escape(name)}'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name='QING')) # /user/QING
    print(url_for('user_page',name='CLEAR')) # /user/CLEAR
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=1))
    return 'Test Page'
