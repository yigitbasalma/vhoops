#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required

from vhoops.modules.teams.api.controllers import get_all_teams_func

from vhoops.modules.on_call.forms.new_on_call import NewOnCallSchedule

on_call_router = Blueprint("on_call_router", __name__)


@on_call_router.route("/on-call", methods=["GET"])
@login_required
def on_call_page():
    # Form config
    teams = get_all_teams_func(as_object=True)
    form = NewOnCallSchedule()
    form.user.choices = [
        (member.id, member.username)
        for team in teams["data"]
        for member in team.members
    ]
    return render_template(
        "on-call/on-call.html",
        teams=teams["data"],
        form=form
    )
