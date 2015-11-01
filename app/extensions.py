# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
bcrypt =  Bcrypt()
