# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from .extensions import login_manager, bootstrap, bcrypt, db


def create_app(config=None):
    app = Flask(__name__)
    configure_app(app, config)
    configure_extensions(app)
    configure_error_handlers(app)
    configure_blueprints(app)
    return app


def configure_app(app, config=None):
    if config:
        app.config.from_object(config)


def configure_extensions(app):
    # Flask-SqlAlchemy
    db.init_app(app)
    # Flask-Bcrypt
    bcrypt.init_app(app)
    # Flask-bootsrap
    bootstrap.init_app(app)
    # Flask-login
    login_manager.login_view = 'auth.login'

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect('/login')
    login_manager.setup_app(app)


def configure_blueprints(app):
    # Configure blueprints in views.
    # register our blueprints
    from home.views import home as home_blueprint
    app.register_blueprint(home_blueprint)
    from auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from panel.views import panel as panel_blueprint
    app.register_blueprint(panel_blueprint)


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden_page.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/server_error.html'), 500
