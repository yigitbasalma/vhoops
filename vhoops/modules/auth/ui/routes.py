#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from vhoops.modules.auth.forms.login import LoginForm

auth_router = Blueprint("auth_router", __name__)


@auth_router.route("/", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_router.user_home_page"))
    return render_template(
        "auth/login.html",
        form=LoginForm()
    )
