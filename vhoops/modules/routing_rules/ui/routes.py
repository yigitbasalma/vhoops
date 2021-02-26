#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from vhoops import authorize, routing_rules_conditions
from vhoops.modules.teams.api.controllers import get_all_teams_func
from vhoops.modules.settings.api.controllers import get_all_integrations_func
from vhoops.modules.alerts.api.models import Alerts

from vhoops.modules.routing_rules.forms.new_rule import RouteDefinition, RuleDefinition, NotificationIntegration
from vhoops.modules.routing_rules.api.controllers import get_all_route_definitions_func

routing_rules_router = Blueprint("routing_rules_router", __name__, url_prefix="/routing-rules")


@routing_rules_router.route("/", methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def routing_rules_page():
    form = RouteDefinition()
    form.team.choices = [(i.id, i.name) for i in get_all_teams_func(as_object=True)["data"]]

    return render_template(
        "routing-rules/routing-rules.html",
        form=form,
        route_definitions=get_all_route_definitions_func(as_object=True)["data"]
    )


@routing_rules_router.route("/<int:route_definition_id>", methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def routing_rule_details_page(route_definition_id):
    route_definition = get_all_route_definitions_func(
        route_definition_id=route_definition_id,
        as_object=True
    )

    if not route_definition["data"]:
        return redirect(url_for("routing_rules_router.routing_rules_page", error="Route Definition not found."))

    route_definition_form = RouteDefinition()
    route_definition_form.team.choices = [(i.id, i.name) for i in get_all_teams_func(as_object=True)["data"]]
    route_definition_form.team.process_data(route_definition["data"][0].team_id)
    route_definition_form.name.data = route_definition["data"][0].name
    route_definition_form.description.data = route_definition["data"][0].description
    route_definition_form.description.render_kw["rows"] = 8
    route_definition_form.status.data = route_definition["data"][0].status

    rule_definition_form = RuleDefinition()
    rule_definition_form.column.choices = [(i, i) for i in Alerts.__searchables__]

    notification_integration_form = NotificationIntegration()
    notification_integration_form.integration.choices = [(i.id, i.name)
                                                         for i in get_all_integrations_func(as_object=True)["data"]]

    return render_template(
        "routing-rules/routing-rule-details.html",
        route_definition=route_definition["data"][0],
        rd_form=route_definition_form,
        rud_form=rule_definition_form,
        ni_form=notification_integration_form,
        rrc=routing_rules_conditions
    )
