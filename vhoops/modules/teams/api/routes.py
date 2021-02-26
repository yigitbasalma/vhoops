#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import authorize, api_version

from vhoops.modules.teams.forms.new_team import NewTeam
from vhoops.modules.teams.api.controllers import get_all_teams_func, create_team_func, remove_team_func

teams_router_api = Blueprint("teams_router_api", __name__, url_prefix=api_version + "/teams")


@teams_router_api.route("/", methods=["POST"])
@authorize.in_group("superuser")
@login_required
def create_new_team():
    form = NewTeam()
    if form.validate():
        return jsonify(
            create_team_func(
                form=form
            )
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@teams_router_api.route("/<int:team_id>/remove", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def remove_team(team_id):
    return jsonify(
        remove_team_func(
            team_id=team_id
        )
    )


@teams_router_api.route("/", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def get_teams():
    return jsonify(
        get_all_teams_func()
    )
