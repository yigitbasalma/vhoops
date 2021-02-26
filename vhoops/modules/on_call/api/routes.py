#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import authorize, api_version
from vhoops.modules.teams.api.controllers import get_all_teams_func

from vhoops.modules.on_call.forms.new_on_call import NewOnCallSchedule
from vhoops.modules.on_call.api.controllers import (
    get_on_call_func,
    create_on_call_schedule_func,
    delete_on_call_schedule_func
)

on_call_router_api = Blueprint("on_call_router_api", __name__, url_prefix=api_version + "/on-call")


@on_call_router_api.route("/", methods=["GET"])
@authorize.in_group("superuser", "team_admin", "user")
@login_required
def get_on_call():
    return jsonify(
        get_on_call_func()
    )


@on_call_router_api.route("/", methods=["POST"])
@authorize.in_group("superuser", "team_admin")
@login_required
def create_on_call_schedule():
    # Form config
    teams = get_all_teams_func(as_object=True)
    form = NewOnCallSchedule()
    form.user.choices = [
        (member.id, member.username)
        for team in teams["data"]
        for member in team.members
    ]
    if form.validate():
        return jsonify(
            create_on_call_schedule_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@on_call_router_api.route("/<int:on_call_id>/remove", methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def delete_on_call_schedule(on_call_id):
    return jsonify(
        delete_on_call_schedule_func(on_call_id=on_call_id)
    )
