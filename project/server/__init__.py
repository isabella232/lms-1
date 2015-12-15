# project/server/__init__.py


###########
# imports #
###########

import os

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy


##########
# config #
##########

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)
app.config.from_object(os.environ['APP_SETTINGS'])


##############
# extensions #
##############

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


##############
# blueprints #
##############

from project.server.main.views import main_blueprint
from project.server.user.views import user_blueprint
from project.server.student.views import student_blueprint
from project.server.teacher.views import teacher_blueprint
from project.server.admin.views import admin_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)
app.register_blueprint(admin_blueprint)


###############
# flask-login #
###############

from project.server.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


##################
# error handlers #
##################

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500