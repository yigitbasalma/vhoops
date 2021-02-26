#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
from sqlalchemy.exc import IntegrityError, OperationalError

from vhoops import db, logging
from vhoops.external.x_tools import generate_id
from vhoops.external.x_exceptions import (
    ResourceError,
    DependencyError,
    ItemNotFoundError,
    ValidationError,
    SecurityError,
    ConditionError
)


def handle_exception(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (ResourceError, DependencyError, ItemNotFoundError, ValidationError, ConditionError) as e:
            logging.write_log(
                event_type=f.__name__,
                event_severity=e[0],
                event=e[1]
            )

            return {
                "status": e[0],
                "message": e[1]
            }
        except (SecurityError, ) as e:
            db.session.rollback()

            logging.write_log(
                event_type=f.__name__,
                event_severity=u"CRITICAL",
                event=e[1]
            )

            return {
                "status": e[0],
                "message": e[1]
            }
        except (IntegrityError, OperationalError) as e:
            db.session.rollback()

            logging.write_log(
                event_type=f.__name__,
                event_severity="ERROR",
                event=e.orig.args
            )

            return {
                "status": "error",
                "message": e.orig.args[1]
            }
        except Exception as e:
            db.session.rollback()

            service_token = generate_id()
            logging.write_log(
                event_type=f.__name__,
                event_severity=u"EXCEPTION",
                event="[{0}] {1}".format(service_token, e)
            )

            return {
                "status": "error",
                "message": str(e)
            }

    return decorated_function
