# -*- coding: utf-8 -*-
from flask import Flask, render_template
from .extensions import login_manager
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    configure_app(app, DevelopmentConfig)
    configure_extensions(app)
    configure_error_handlers(app)
    configure_blueprints(app)
    return app


def configure_app(app,config=None):
    if config:
        app.config.from_object(config)


def configure_extensions(app):
    # flask-login
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.reauth'

    @login_manager.user_loader
    def load_user(id):
        pass
        # return User.query.get(id)

    @login_manager.unauthorized_handler
    def unauthorized():
        pass
        # return redirect('/login')
    login_manager.setup_app(app)


def configure_blueprints(app):
    # Configure blueprints in views.
    # register our blueprints
    from home.views import home as home_blueprint
    app.register_blueprint(home_blueprint)


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
