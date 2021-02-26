#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

from vhoops import api_version

from vhoops.modules.auth.forms.login import LoginForm
from vhoops.modules.auth.api.controllers import login_user, logout_user

auth_router_api = Blueprint("auth_router_api", __name__, url_prefix=api_version + "/auth")


@auth_router_api.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        return jsonify(
            login_user(
                form=form,
            )
        )
    return jsonify({
        "status": "error",
        "error": f"{form.errors}"
    })


@auth_router_api.route("/logout", methods=["GET"])
def logout():
    return logout_user()
