#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required

from vhoops import authorize

from vhoops.modules.teams.forms.new_team import NewTeam

teams_router = Blueprint("teams_router", __name__)


@teams_router.route("/teams", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def teams_page():
    return render_template(
        "teams/teams.html",
        form=NewTeam()
    )
