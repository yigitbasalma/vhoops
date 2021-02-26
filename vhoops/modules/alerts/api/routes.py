#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask_login import login_required

from vhoops import authorize, api_version
from vhoops.wrappers.mixed_login import mixed_login

from vhoops.modules.alerts.forms.new_alert import NewAlert
from vhoops.modules.alerts.forms.new_comment import NewComment
from vhoops.modules.alerts.api.controllers import (
    get_alerts_func,
    create_new_alert_func,
    create_comment_for_alert_func,
    change_ack_status_func,
    close_alert_func
)

alerts_router_api = Blueprint("alerts_router_api", __name__, url_prefix=api_version + "/alerts")


@alerts_router_api.route("/", methods=["GET"])
@authorize.in_group("superuser", "team_admin", "user")
@login_required
def get_alerts():
    return jsonify(
        get_alerts_func(
            filters=request.args.get("filters")
        )
    )


@alerts_router_api.route("/<int:alert_id>", methods=["GET"])
@authorize.in_group("superuser", "team_admin", "user")
@login_required
def get_alert_by_id(alert_id):
    return jsonify(
        get_alerts_func(alert_id=alert_id)
    )


@alerts_router_api.route("/", methods=["POST"])
@mixed_login
def create_alert_record(is_api):
    meta = dict()
    if is_api:
        meta["csrf"] = False

    form = NewAlert(meta=meta)
    if form.validate():
        return jsonify(
            create_new_alert_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@alerts_router_api.route("/<int:alert_id>/comment", methods=["POST"])
@mixed_login
def create_alert_comment(is_api, alert_id):
    meta = dict()
    if is_api:
        meta["csrf"] = False

    form = NewComment(meta=meta)
    if form.validate():
        return jsonify(
            create_comment_for_alert_func(form=form, alert_id=alert_id)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@alerts_router_api.route("/<int:alert_id>/acknowledge", methods=["PUT", "DELETE"])
@mixed_login
def acknowledge_alert(_, alert_id):
    if request.method == "PUT":
        return jsonify(
            change_ack_status_func(alert_id=alert_id, state="ack")
        )
    return jsonify(
        change_ack_status_func(alert_id=alert_id, state="un-ack")
    )


@alerts_router_api.route("/<int:alert_id>", methods=["PUT"])
@mixed_login
def close_alert(_, alert_id):
    return jsonify(
        close_alert_func(
            alert_id=alert_id
        )
    )
