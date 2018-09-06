#!/usr/bin/env python
import os
from app import create_app
#from app.models import Admin, Post, Tag, Category, SiteLink, \
#    Page, LoveMe, Comment, Shuoshuo, SideBox
from app.home.views import availablePort,register,getport,getuser
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()
#app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
#migrate = Migrate(app, db)

# if os.path.exists('.env'):
#     for line in open('.env'):
#         var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]
            
#每次启动shell会话都要导入Python相关对象（数据库实例和模型），这是件十分枯燥的工作。
#为了避免一直重复导入，我们可以做些配置，让flask-script的shell命令自动导入特定的对象。

def make_shell_context():
    # return dict(app=app, db=db, Admin=Admin, Post=Post, Tag=Tag,
    #         Category=Category, SiteLink=SiteLink, Page=Page,
    #         LoveMe=LoveMe, Comment=Comment, Shuoshuo=Shuoshuo, SideBox=SideBox)
    return dict(app=app, availablePort=availablePort, register=register,getport=getport,
    	getuser=getuser)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

#先创建迁移仓库：python manage.py db init
#创建迁移脚本，migrate子命令用来自动创建：python manage.py db migrate -m "v1.0"
#更新数据库操作：python manage.py db upgrade
#创建管理员信息：python manage.py addAdmin

# @manager.command
# def clearAlembic():
#     from app.models import Alembic
#     Alembic.clear_A()

# @manager.command
# def addAdmin():
#     from app.models import Admin, LoveMe
#     from config import Config
#     # 创建管理员
#     admin = Admin(site_name=Config.SITE_NAME, site_title=Config.SITE_TITLE ,name=Config.ADMIN_NAME,
#                   profile=Config.ADMIN_PROFILE, login_name=Config.ADMIN_LOGIN_NAME,
#                   password=Config.ADMIN_PASSWORD)
#     # 创建love-me
#     love = LoveMe(loveMe=666)
#     # 创建留言板
#     guestbook = Page(title='leave a message', url_name='guestbook', canComment=True, isNav=False,
#                      body='leave a message')
#     db.session.add(admin)
#     db.session.add(love)
#     db.session.add(guestbook)
#     db.session.commit()


if __name__ == '__main__':
    manager.run()
