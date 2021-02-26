#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import authorize, api_version

from vhoops.modules.settings.forms.new_integration import NewIntegration
from vhoops.modules.settings.api.controllers import create_new_integration_func, update_integration_func

settings_router_api = Blueprint("settings_router_api", __name__, url_prefix=api_version + "/settings")


@settings_router_api.route("/output-integrations", methods=["POST"])
@authorize.in_group("superuser")
@login_required
def create_new_integration():
    form = NewIntegration()
    if form.validate():
        return jsonify(
            create_new_integration_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@settings_router_api.route("/output-integrations/<int:integration_id>", methods=["POST"])
@authorize.in_group("superuser")
@login_required
def update_integration(integration_id):
    form = NewIntegration()
    # Define fake identifier for validation. This value is already ignored.
    form.identifier.data = "fake_identifier"
    if form.validate():
        return jsonify(
            update_integration_func(form=form, integration_id=integration_id)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })
