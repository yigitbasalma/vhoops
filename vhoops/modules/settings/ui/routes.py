#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from vhoops import authorize
from vhoops.external.x_tools import pretty_json

from vhoops.modules.settings.forms.new_integration import NewIntegration
from vhoops.modules.settings.api.controllers import get_all_integrations_func

settings_router = Blueprint("settings_router", __name__, url_prefix="/settings")


@settings_router.route("/output-integrations", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def output_integration_page():
    form = NewIntegration()
    return render_template(
        "settings/output-integrations.html",
        form=form,
        integrations=get_all_integrations_func(as_object=True)["data"]
    )


@settings_router.route("/output-integrations/<int:integration_id>", methods=["GET"])
@authorize.in_group("superuser")
@login_required
def output_integration_details_page(integration_id):
    integration = get_all_integrations_func(integration_id=integration_id, as_object=True)

    if not integration["data"]:
        return redirect(url_for("settings_router.output_integration_page", error="Integration not found"))

    form = NewIntegration()
    form.name.data = integration["data"][0].name
    form.integration_icon.data = integration["data"][0].icon_url
    form.config.data = pretty_json(integration["data"][0].config)
    form.fields.data = pretty_json(integration["data"][0].fields)
    form.is_available.data = integration["data"][0].is_available

    return render_template(
        "settings/output-integration-edit.html",
        form=form,
        integration=integration["data"][0]
    )
