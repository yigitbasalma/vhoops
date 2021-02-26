#!/usr/bin/python
# -*- coding: utf-8 -*-

from vhoops.external.x_tools import calculate_hash, datetime_pattern

# Statement for enabling the development environment
DEBUG = True

# Running env
ENV = "development"

# Logging config
LOGGING_BASE = "/var/log/vhoops"
LOG_LEVEL = "INFO"

# Session manager config
SESSION_TYPE = "mongodb"
SESSION_MONGODB = "mongodb://watchmon:Qazxsw123*@192.168.56.2"

# SQLAlchemy Config
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@192.168.56.2:3306/vhoops"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 120,
    "pool_pre_ping": True
}


# Mail config
MAIL_USERNAME = "vhoops@vhoops.com"
MAIL_PASSWORD = "123456"
MAIL_SERVER = "smtp.mail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = "vhoops-donotreply"

# NoSQL config
CACHE_CONN_STRING = "couchbase://192.168.56.2"
CACHE_USERNAME = "Administrator"
CACHE_PASSWORD = "123456*"
CACHE_BUCKETS = [
    "app_cache"
]

# Cache config
CACHE_TYPE = "redis"
CACHE_REDIS_HOST = "192.168.56.2"

# Queue config
CELERY_BROKER_URL = "redis://192.168.56.2:6379/1"

# Session config
PERMANENT_SESSION_LIFETIME = 3000

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "1vAM_*!K_!9_+__V~~asd123!^+2345_:|44*qn.6V.=32.~|m!_|2H2Uz7wIg9Y1IV"

# Secret key for signing cookies
SECRET_KEY = "^740*4X7B4F.0gn0c21f69~_s|1vAM_*!K_::-*I8-9|i7|*S4W2^7|z*H24.tP"

# Re-captcha settings
RECAPTCHA_SITE_KEY = "6LdHbpkUAAAAAJgCqUYg_FMNtFvNvUgb4GpRMcv4"
RECAPTCHA_SECRET_KEY = "6LdHbpkUAAAAAMznQYxYxy52LmC7ohAR-W0qXV2T"
RECAPTCHA_ENABLED = False

# Folder bases
USER_BASE = "/opt/vhoops/user-base"
EMAIL_TEMPLATE_BASE = "static/assets/email-templates"
TEMP_DIR = "/opt/vhoops/tmp"

# General config
BASE_URL = "vhoops.org"
API_VERSION = "/api/v1"

# Application config
PAGE_CONFIG = dict(
    PAGE_TITLE="Vhoops Alert Router",
    BRAND_NAME="Vhoops",
    COPYRIGHTS=datetime_pattern("copyrights")
)
ROOT_USER_DATA = dict(
    id=1,
    first_name="root",
    last_name="root",
    username="root",  # Must be a root
    email="root@local.com",
    password=calculate_hash("123456")
)
ROOT_GROUP_DATA = dict(
    name="superuser",
    allowances=dict(),
    description="Superuser group."
)
INITIAL_GROUPS_DATA = [
    dict(
        name="team_admin",
        allowances=dict(),
        description="Team admin group."
    ),
    dict(
        name="user",
        allowances=dict(),
        description="Standard user group."
    ),
    dict(
        name="api_user",
        allowances=dict(),
        description="Standard api user group (Cannot UI access)."
    )
]
PRIORITIES = {
    "P1": "",
    "P2": "",
    "P3": "",
    "P4": "",
    "P5": ""
}
ROUTING_RULE_CONDITIONS = {
    "regex_match": "Matches (Regex)",
    "eq": "Equals",
    "gt": "Greater Than",
    "contains": "Contains",
    "starts_with": "Starts With",
    "ends_with": "Ends With",
    "is_empty": "Is Empty"
}
