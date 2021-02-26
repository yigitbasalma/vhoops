#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from vhoops.modules.alerts.forms.new_comment import NewComment
from vhoops.modules.alerts.api.controllers import get_alerts_func, mark_as_seen_func

alerts_router = Blueprint("alerts_router", __name__)


@alerts_router.route("/alerts", methods=["GET"])
@login_required
def alerts_page():
    return render_template(
        "alerts/alerts.html",
        alerts=get_alerts_func(
            as_object=True,
            filters=request.args.get("filters")
        )["data"]
    )


@alerts_router.route("/alerts/<int:alert_id>", methods=["GET"])
@login_required
def alert_details_page(alert_id):
    alert = get_alerts_func(alert_id=alert_id, as_object=True)

    if not alert["data"]:
        return redirect(url_for("alerts_router.alerts_page", error="Alert not found"))

    mark_as_seen_func(alert=alert["data"][0])

    return render_template(
        "alerts/alert-details.html",
        alert=alert["data"][0],
        form=NewComment()
    )
