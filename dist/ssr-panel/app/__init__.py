from flask import Flask
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import os


#app = Flask(__name__)
def create_app():
	app = Flask(__name__)
	app.debug = False
	app.config['SECRET_KEY'] = '183449eb77e74f5e8c2023d09a1c1734'
	from app.admin import admin as admin_blueprint
	from app.home import home as home_blueprint

	# manager = Manager(app)



	app.register_blueprint(home_blueprint)
	# prefix /admin to url to sperate from general user
	app.register_blueprint(admin_blueprint, url_prefix = '/admin') 

	# def make_shell_context():
	# return dict(app=app)
	# manager.add_command("shell", Shell(make_context=make_shell_context))
	return app
