#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, desc
from flask_login import current_user

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception, ItemNotFoundError, DependencyError

from vhoops.modules.teams.api.models import Teams


@handle_exception
def get_all_teams_func(team_id=None, as_object=False):
    query = Teams.query
    query_filters = list()

    if team_id:
        query_filters.append(
            Teams.id == team_id
        )

    if not current_user.has_group("superuser"):
        query_filters.append(
            Teams.id.in_([i.id for i in current_user.teams])
        )

    return {
        "data": [
            i.as_dict if not as_object else i
            for i in query.filter(and_(*query_filters)).order_by(desc(Teams.registration_timestamp)).all()
        ]
    }


@handle_exception
def create_team_func(form):
    db.session.add(
        Teams(
            name=form.name.data,
            description=form.description.data.capitalize()
        )
    )
    db.session.commit()

    logging.write_log(
        event_type=u"create_team",
        event_severity=u"INFO",
        event=f"'{form.name.data}' team created."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Team created."
    }


@handle_exception
def remove_team_func(team_id):
    team = Teams.query.filter_by(id=team_id).first()

    if not team:
        raise ItemNotFoundError("error", "Team not found.")

    if team.members:
        raise DependencyError("error", "Team has members. Please remove members first.")

    db.session.delete(team)
    db.session.commit()

    logging.write_log(
        event_type=u"remove_team",
        event_severity=u"INFO",
        event=f"'{team.name}' team removed."
    )

    return {
        "status": "success",
        "message": "Team removed."
    }
