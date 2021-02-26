#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from vhoops import authorize, api_version
from vhoops.modules.teams.api.controllers import get_all_teams_func
from vhoops.modules.settings.api.controllers import get_all_integrations_func
from vhoops.modules.alerts.api.models import Alerts

from vhoops.modules.routing_rules.forms.new_rule import RouteDefinition, RuleDefinition, NotificationIntegration
from vhoops.modules.routing_rules.api.controllers import (
    create_new_route_definition_func,
    update_route_definition_func,
    create_route_definition_rule_func,
    remove_route_definition_rule_func,
    remove_route_definition_func,
    create_route_definition_notification_integration_func,
    remove_route_definition_notification_integration_func
)

routing_rules_router_api = Blueprint("routing_rules_router_api", __name__, url_prefix=api_version + "/routing-rules")


@routing_rules_router_api.route("/", methods=["POST"])
@authorize.in_group("superuser", "team_admin")
@login_required
def create_new_route_definition():
    form = RouteDefinition()
    form.team.choices = [(i.id, i.name) for i in get_all_teams_func(as_object=True)["data"]]

    if form.validate():
        return jsonify(
            create_new_route_definition_func(form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@routing_rules_router_api.route("/<int:route_definition_id>", methods=["POST"])
@authorize.in_group("superuser", "team_admin")
@login_required
def update_route_definition(route_definition_id):
    form = RouteDefinition()
    form.team.choices = [(i.id, i.name) for i in get_all_teams_func(as_object=True)["data"]]

    if form.validate():
        return jsonify(
            update_route_definition_func(route_definition_id=route_definition_id, form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@routing_rules_router_api.route("/<int:route_definition_id>/remove", methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def delete_route_definition(route_definition_id):
    return jsonify(
        remove_route_definition_func(route_definition_id=route_definition_id)
    )


@routing_rules_router_api.route("/<int:route_definition_id>/rules", methods=["POST"])
@authorize.in_group("superuser", "team_admin")
@login_required
def create_route_definition_rule(route_definition_id):
    form = RuleDefinition()
    form.column.choices = [(i, i) for i in Alerts.__searchables__]

    if form.validate():
        return jsonify(
            create_route_definition_rule_func(route_definition_id=route_definition_id, form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@routing_rules_router_api.route("/<int:route_definition_id>/rules/<int:rule_id>/remove", methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def delete_route_definition_rule(route_definition_id, rule_id):
    return jsonify(
        remove_route_definition_rule_func(route_definition_id=route_definition_id, rule_id=rule_id)
    )


@routing_rules_router_api.route("/<int:route_definition_id>/notification-integrations", methods=["POST"])
@authorize.in_group("superuser", "team_admin")
@login_required
def create_route_definition_notification_integration(route_definition_id):
    form = NotificationIntegration()
    form.integration.choices = [(i.id, i.name) for i in get_all_integrations_func(as_object=True)["data"]]

    if form.validate():
        return jsonify(
            create_route_definition_notification_integration_func(route_definition_id=route_definition_id, form=form)
        )

    return jsonify({
        "status": "error",
        "message": f"{form.errors}"
    })


@routing_rules_router_api.route("/<int:route_definition_id>/notification-integrations/<int:rule_id>/remove",
                                methods=["GET"])
@authorize.in_group("superuser", "team_admin")
@login_required
def delete_route_definition_notification_integration(route_definition_id, rule_id):
    return jsonify(
        remove_route_definition_notification_integration_func(route_definition_id=route_definition_id, rule_id=rule_id)
    )
