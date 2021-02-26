#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import api_version

from vhoops.modules.home.forms.user_profile import General, ChangePassword
from vhoops.modules.home.api.controllers import update_user_profile_generals_func, update_user_password_change_func

home_router_api = Blueprint("home_router_api", __name__, url_prefix=api_version + "/home")


@home_router_api.route("/user-profile/generals", methods=["POST"])
@login_required
def update_user_profile_generals():
    form = General()
    if form.validate():
        return jsonify(
            update_user_profile_generals_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@home_router_api.route("/user-profile/password-change", methods=["POST"])
@login_required
def update_user_password_change():
    form = ChangePassword()
    if form.validate():
        return jsonify(
            update_user_password_change_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })
