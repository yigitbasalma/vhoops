#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_
from flask_login import current_user

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import ItemNotFoundError, ConditionError
from vhoops.external.x_tools import datetime_pattern
from vhoops.modules.auth.api.models import Users

from vhoops.modules.on_call.api.models import OnCall


@handle_exception
def get_on_call_func(on_call_id=None, as_object=False):
    query = OnCall.query
    query_filters = list()

    if on_call_id:
        query_filters.append(
            OnCall.id == on_call_id
        )

    if not current_user.has_group("superuser"):
        query_filters.append(
            OnCall.team_id.in_([i.id for i in current_user.teams])
        )

    return {
        "data": [
            i.as_dict if not as_object else i
            for i in query.filter(and_(*query_filters)).all()
        ]
    }


@handle_exception
def create_on_call_schedule_func(form):
    # Define variables
    user_id = form.user.data
    start_date = form.start_date.data
    end_date = form.end_date.data

    user = Users.query.filter_by(id=user_id).first()
    user_on_call = OnCall.query.filter(
        and_(
            OnCall.user_id == user_id,
            db.func.date_format(OnCall.start, "%Y-%m-%d") == datetime_pattern(pt="date", dt=start_date)
        )
    ).first()

    if not user:
        raise ItemNotFoundError("error", "User not found.")

    if datetime_pattern(pt="js", dt=start_date) < datetime_pattern(pt="js"):
        raise ConditionError("error", "You cannot enter old dated records.")

    if start_date > end_date:
        raise ConditionError("error", "Start date couldn't be greater than end date.")

    if (end_date - start_date).total_seconds() < 86400:  # 1 day = 86400 seconds
        raise ConditionError("error", "On-Call records must be at least 24 hours.")

    if user_on_call:
        raise ConditionError("error", "User already on-call in start date.")

    db.session.add(
        OnCall(
            user_id=user.id,
            team_id=user.teams[0].id,
            start=start_date,
            end=end_date
        )
    )
    db.session.commit()

    logging.write_log(
        event_type=u"create_on_call_schedule",
        event_severity=u"INFO",
        event=f"'{user.username}' on-call schedule created."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "On-Call schedule created."
    }


@handle_exception
def delete_on_call_schedule_func(on_call_id):
    on_call = get_on_call_func(on_call_id=on_call_id, as_object=True)

    if not on_call["data"]:
        raise ItemNotFoundError("error", "On-Call schedule not found.")

    on_call_object = on_call["data"][0]

    if on_call_object.end < datetime_pattern(skip_format=True):
        raise ConditionError("error", "You cannot delete old dated records.")

    if on_call_object.start < datetime_pattern(skip_format=True) < on_call_object.end:
        on_call_object.end = db.func.current_timestamp()
    else:
        db.session.delete(on_call_object)

    db.session.commit()

    logging.write_log(
        event_type=u"delete_on_call_schedule",
        event_severity=u"INFO",
        event=f"'{on_call_object.user.username}-{on_call_object.start}-{on_call_object.end}' on-call schedule deleted."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "On-Call schedule deleted."
    }
