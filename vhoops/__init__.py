#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_caching import Cache
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_authorize import Authorize
from flask_mail import Mail
from celery import Celery

from vhoops.external.x_tools import datetime_pattern
from vhoops.external.x_in_memory_cache import NoSQL
from vhoops.external.x_logging import Logger

# Define the WSGI application object
app = Flask(__name__)

# Set project base
project_base = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config.from_object("vhoops.config.dev")
if os.path.exists(os.path.join(os.getcwd(), "vhoops/config/config.py")):
    app.config.from_object("vhoops.config.config")

# SQLAlchemy init
db = SQLAlchemy(app)

# LoginManager init
login_manager = LoginManager(app)

# AuthorizeManager init
authorize = Authorize(app)

# Migration controller init
migrate = Migrate(app, db)

# Create session interface
Session(app)

# Cache init
cache = Cache(app)

# Bootstrapping init
Bootstrap(app)

# Couchbase buckets init
app_cache = NoSQL(app)

# Mail init
email = Mail(app)

# Logging init
logging = Logger(app)


# Create Database base model
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    registration_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def base_filters(self):
        return [
            self.team_id.in_([i.id for i in current_user.teams])
        ] if not (getattr(self, "team_id") and current_user.has_group("superuser")) else list()


def make_celery(_app):
    from vhoops.config import celery_config
    _celery = Celery(
        _app.import_name,
        broker=_app.config['CELERY_BROKER_URL']
    )
    _celery.conf.update(_app.config)
    _celery.config_from_object(celery_config)

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with _app.app_context():
                return self.run(*args, **kwargs)

    _celery.Task = ContextTask
    return _celery


# Backend job controller init
celery = make_celery(app)


# User loader for LoginManager
from vhoops.modules.auth.api.models import Users


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_router.login"))


# Error handlers
app.register_error_handler(401, lambda _: redirect(url_for("auth_router.login")))


# Set base configurations
api_version = app.config["API_VERSION"]
alert_priorities = app.config["PRIORITIES"]
user_groups = app.config["INITIAL_GROUPS_DATA"]
routing_rules_conditions = app.config["ROUTING_RULE_CONDITIONS"]

# Set base folders
email_template_base = os.path.join(project_base, app.config["EMAIL_TEMPLATE_BASE"])
user_base = app.config["USER_BASE"]
temp_dir = app.config["TEMP_DIR"]
base_url = app.config["BASE_URL"]


# Constraint values
@app.context_processor
def constraints():
    return app.config["PAGE_CONFIG"]


if app:
    db.create_all()

    # UI Pages
    from vhoops.modules.auth.ui.routes import auth_router
    from vhoops.modules.home.ui.routes import home_router
    from vhoops.modules.alerts.ui.routes import alerts_router
    from vhoops.modules.teams.ui.routes import teams_router
    from vhoops.modules.users.ui.routes import users_router
    from vhoops.modules.on_call.ui.routes import on_call_router
    from vhoops.modules.settings.ui.routes import settings_router
    from vhoops.modules.routing_rules.ui.routes import routing_rules_router

    # API Pages
    from vhoops.modules.auth.api.routes import auth_router_api
    from vhoops.modules.teams.api.routes import teams_router_api
    from vhoops.modules.users.api.routes import users_router_api
    from vhoops.modules.alerts.api.routes import alerts_router_api
    from vhoops.modules.home.api.routes import home_router_api
    from vhoops.modules.on_call.api.routes import on_call_router_api
    from vhoops.modules.settings.api.routes import settings_router_api
    from vhoops.modules.routing_rules.api.routes import routing_rules_router_api

    # Analytics API
    from vhoops.modules.analytics.api.routes import analytics_router_api

    # Add blueprints of ui pages
    app.register_blueprint(auth_router)
    app.register_blueprint(home_router)
    app.register_blueprint(alerts_router)
    app.register_blueprint(teams_router)
    app.register_blueprint(users_router)
    app.register_blueprint(on_call_router)
    app.register_blueprint(settings_router)
    app.register_blueprint(routing_rules_router)

    # Add blueprints of api pages
    app.register_blueprint(auth_router_api)
    app.register_blueprint(teams_router_api)
    app.register_blueprint(users_router_api)
    app.register_blueprint(alerts_router_api)
    app.register_blueprint(home_router_api)
    app.register_blueprint(on_call_router_api)
    app.register_blueprint(settings_router_api)
    app.register_blueprint(routing_rules_router_api)

    # Add blueprints for analytic api page
    app.register_blueprint(analytics_router_api)

db.create_all()
