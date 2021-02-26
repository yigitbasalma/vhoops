#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta
from sqlalchemy import and_
from flask import url_for, redirect
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout_user

from vhoops import logging
from vhoops.external.x_tools import calculate_hash
from vhoops.external.x_exceptions import SecurityError, ValidationError
from vhoops.wrappers.exceptions import handle_exception

from vhoops.modules.auth.api.models import Users


@handle_exception
def login_user(form):
    username = form.username.data
    password = calculate_hash(form.password.data)
    user_object = Users.query.filter(
        and_(
            Users.username == username,
            Users.password == password
        )
    ).first()

    if not user_object:
        raise SecurityError("error", f"Wrong username or password for '{username}'")

    # Check customer account status
    if not user_object.account_status:
        raise SecurityError("error", "Your account status is not suitable for login. Please contact us.")

    if "api_user" in [i.as_dict["name"] for i in user_object.groups]:
        raise ValidationError("error", "Your account group is api_user. You cannot login UI.")

    # Define session
    flask_login_user(
        user=user_object,
        remember=form.remember_me.data,
        duration=timedelta(days=90)
    )

    logging.write_log(
        event_type=u"login_user",
        event_severity=u"INFO",
        event=f"Successfully login."
    )

    return {
        "status": "success",
        "message": "Successful login.",
        "redirect": url_for("home_router.user_home_page")
    }


@handle_exception
def logout_user():
    logging.write_log(
        event_type=u"logout_user",
        event_severity=u"INFO",
        event=f"Successfully logout."
    )
    flask_logout_user()
    return redirect(url_for("auth_router.login"))
