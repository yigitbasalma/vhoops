#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_
from flask_login import current_user

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import SecurityError, ValidationError
from vhoops.external.x_tools import calculate_hash

from vhoops.modules.auth.api.models import Users


@handle_exception
def update_user_profile_generals_func(form):
    # Define variables
    first_name = form.first_name.data.title()
    last_name = form.last_name.data.upper()
    email = form.email.data
    phone = form.phone.data

    user = Users.query.filter_by(id=current_user.id).first()

    if not user:
        raise SecurityError("error", "Critical action.")

    if user.first_name != first_name:
        user.first_name = first_name

    if user.last_name != last_name:
        user.last_name = last_name

    if user.email != email:
        user.email = email

    if user.phone_number != phone:
        user.phone_number = phone

    db.session.commit()

    logging.write_log(
        event_type=u"update_user_profile_generals",
        event_severity=u"INFO",
        event="Profile updated."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Profile updated."
    }


@handle_exception
def update_user_password_change_func(form):
    # Define variables
    old_password = calculate_hash(form.old_password.data)
    new_password = calculate_hash(form.new_password.data)
    retype_new_password = calculate_hash(form.retype_new_password.data)

    user = Users.query.filter(
        and_(
            Users.id == current_user.id,
            Users.password == old_password
        )
    ).first()

    if not user:
        raise SecurityError("error", "Incorrect password for user.")

    if new_password != retype_new_password:
        raise ValidationError("error", "Passwords does not match.")

    user.password = new_password

    db.session.commit()

    logging.write_log(
        event_type=u"update_user_password",
        event_severity=u"INFO",
        event="Password updated."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Password updated."
    }
