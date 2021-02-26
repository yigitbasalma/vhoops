#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import authorize, api_version, user_groups
from vhoops.modules.teams.api.models import Teams

from vhoops.modules.users.forms.new_user import NewUser
from vhoops.modules.users.api.controllers import get_all_users_func, create_user_func, remove_user_func

users_router_api = Blueprint("users_router_api", __name__, url_prefix=api_version + "/users")


@users_router_api.route("/", methods=["POST"])
@authorize.in_group("superuser")
@login_required
def create_new_user():
    form = NewUser()
    form.teams.choices.extend((i.as_dict['name'], i.as_dict['name']) for i in Teams.query.all())
    form.group.choices.extend((i['name'], i['name']) for i in user_groups)
    if form.validate():
        return jsonify(
            create_user_func(
                form=form
            )
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@users_router_api.route("/<int:user_id>/remove", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def remove_user(user_id):
    return jsonify(
        remove_user_func(
            user_id=user_id
        )
    )


@users_router_api.route("/", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def get_users():
    return jsonify(
        get_all_users_func()
    )
