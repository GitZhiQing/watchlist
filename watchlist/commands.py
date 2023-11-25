# 命令函数，定义了三个 Flask 命令行接口（CLI）命令：initdb、forge 和 admin。分别用于初始化数据库、生成虚拟数据和设置管理员账户。

"""导入
导入所需的库和模块。这包括 click（用于创建命令行接口），app 和 db（从 watchlist 模块中导入的 Flask 应用实例和 SQLAlchemy 实例），User 和 Movie（从 watchlist.models 模块中导入的用户和电影模型）。
"""

import click
from watchlist import app, db
from watchlist.models import User, Movie


# initdb 命令函数，用于初始化数据库；--drop 选项，用于在创建数据库之前删除已存在的同名数据库。
@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


# forge 命令函数，用于生成模型类的虚拟数据。
# 两个表 user movie
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = "Grey Li"
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m["title"], year=m["year"])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")


# admin 命令函数，用于生成管理员账户。
# --username 和 --password 选项，用于输入用户名和密码。
@app.cli.command()
@click.option("--username", prompt=True, help="The username used to login.")
@click.option(
    "--password",
    prompt=True,  # 提示用户输入
    hide_input=True,  # 隐藏用户输入
    confirmation_prompt=True,  # 再次确认
    help="The password used to login.",  # 帮助文本
)
def admin(username, password):
    """Create user."""
    db.create_all()
    # 取 user 表中的第一条数据，如果存在则更新，否则创建
    user = User.query.first()
    if user is not None:
        # 如果存在则更新
        click.echo("Updating user...")
        # 更新 username 字段和 password 字段
        user.username = username
        user.set_password(password)
    else:
        # 否则创建
        click.echo("Creating user...")
        # 创建用户，更新 username 字段和 password 字段，设置 name 字段为默认值 Admin
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo("Done.")
