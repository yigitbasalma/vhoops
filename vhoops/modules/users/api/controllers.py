#!/usr/bin/python
# -*- coding: utf-8 -*-

from vhoops import app, db, logging
from vhoops.wrappers.exceptions import handle_exception, ItemNotFoundError
from vhoops.external.x_tools import strong_password, calculate_hash

from vhoops.modules.auth.api.models import Users, Groups
from vhoops.modules.teams.api.models import Teams


@handle_exception
def get_all_users_func():
    return {
        "data": [
            i.as_dict
            for i in Users.query.filter(
                Users.username != app.config["ROOT_USER_DATA"]["username"]
            ).all()
        ]
    }


@handle_exception
def create_user_func(form):
    group = Groups.query.filter_by(
        name=form.group.data
    ).first()

    teams = Teams.query.filter(
        Teams.name.in_(form.teams.data)
    ).all()

    user_password = strong_password()

    db.session.add(
        Users(
            first_name=form.first_name.data.title(),
            last_name=form.last_name.data.upper(),
            username=form.username.data.lower(),
            email=form.email.data,
            phone_number=form.phone.data.replace("+", ""),
            groups=[group],
            teams=teams,
            password=calculate_hash(user_password)
        )
    )
    db.session.commit()

    logging.write_log(
        event_type=u"create_user",
        event_severity=u"INFO",
        event=f"'{form.username.data}' user created. Password: {user_password}"
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "User created."
    }


@handle_exception
def remove_user_func(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        raise ItemNotFoundError("error", "User not found.")

    db.session.delete(user)
    db.session.commit()

    logging.write_log(
        event_type=u"remove_user",
        event_severity=u"INFO",
        event=f"'{user.username}' user removed."
    )

    return {
        "status": "success",
        "message": "User removed."
    }
