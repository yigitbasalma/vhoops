#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required

from vhoops import authorize, user_groups
from vhoops.modules.users.forms.new_user import NewUser
from vhoops.modules.teams.api.models import Teams

users_router = Blueprint("users_router", __name__)


@users_router.route("/users", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def users_page():
    new_user_form = NewUser()
    new_user_form.teams.choices.extend((i.as_dict['name'], i.as_dict['name']) for i in Teams.query.all())
    new_user_form.group.choices.extend((i['name'], i['name']) for i in user_groups)
    return render_template(
        "users/users.html",
        form=new_user_form
    )
