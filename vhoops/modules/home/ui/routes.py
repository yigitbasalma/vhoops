#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from vhoops.modules.home.forms.user_profile import General, ChangePassword

from vhoops.modules.alerts.api.controllers import get_alerts_func
from vhoops.modules.teams.api.controllers import get_all_teams_func
from vhoops.modules.users.api.controllers import get_all_users_func

home_router = Blueprint("home_router", __name__)


@home_router.route("/home", methods=["GET"])
@login_required
def user_home_page():
    return render_template(
        "home/home-page.html",
        alerts=get_alerts_func(filters="status:open"),
        teams=get_all_teams_func(),
        users=get_all_users_func()
    )


@home_router.route("/profile", methods=["GET"])
@login_required
def user_profile_page():
    # General section form
    form_general = General()
    form_general.first_name.render_kw["value"] = current_user.first_name
    form_general.last_name.render_kw["value"] = current_user.last_name
    form_general.email.render_kw["value"] = current_user.email
    form_general.phone.render_kw["value"] = current_user.phone_number

    # Change password section form
    change_password_form = ChangePassword()

    return render_template(
        "home/user-profile.html",
        form_general=form_general,
        change_password_form=change_password_form
    )
