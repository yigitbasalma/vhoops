#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os

from flask import request
from flask_login import current_user

from vhoops.external.x_tools import datetime_pattern


class Logger(object):
    def __init__(self, app):
        logger = logging.getLogger("Vhoops")
        handler = logging.FileHandler(os.path.join(app.config["LOGGING_BASE"], "application.log"))
        formatter = logging.Formatter(
            u"%(custom_timestamp)s %(event_type)s %(event_ip)s %(levelname)s %(event_user)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.getLevelName(app.config["LOG_LEVEL"]))
        self.logging_convert_table = {
            "INFO": logger.info,
            "ERROR": logger.error,
            "WARNING": logger.warning,
            "CRITICAL": logger.critical,
            "EXCEPTION": logger.exception
        }

    def write_log(self, event_type, event_severity, event, user="system"):
        # For file log
        event_severity = event_severity.upper()
        logger_extras = {
            "custom_timestamp": datetime_pattern(),
            "event_type": event_type,
            "event_ip": request.headers.get("X-Forwarded-For", "127.0.0.1"),
            "event_user": current_user.username if current_user.is_authenticated else user
        }
        self.logging_convert_table[event_severity](event, extra=logger_extras,
                                                   exc_info=True if event_severity in ["EXCEPTION"] else False)
