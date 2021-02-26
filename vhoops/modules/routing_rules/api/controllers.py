#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, desc
from flask_login import current_user

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import SecurityError, ItemNotFoundError, DependencyError
from vhoops.modules.settings.api.controllers import get_all_integrations_func

from vhoops.modules.routing_rules.api.models import Routes, Rules, NotificationIntegrations


@handle_exception
def get_all_route_definitions_func(route_definition_id=None, as_object=False):
    query = Routes.query
    query_filters = list()

    if route_definition_id:
        query_filters.append(
            Routes.id == route_definition_id
        )

    if not current_user.has_group("superuser"):
        query_filters.append(
            Routes.team_id.in_([i.id for i in current_user.teams])
        )

    return {
        "data": [
            i.as_dict if not as_object else i
            for i in query.filter(and_(*query_filters)).order_by(desc(Routes.registration_timestamp)).all()
        ]
    }


@handle_exception
def create_new_route_definition_func(form):
    # Define variables
    name = form.name.data.title()
    description = form.description.data.capitalize()
    team_id = form.team.data

    if not current_user.has_group("superuser"):
        if team_id not in [i.id for i in current_user.teams]:
            raise SecurityError("error", "Unauthorized action attempted.")

    db.session.add(Routes(
        name=name,
        description=description,
        team_id=team_id
    ))
    db.session.commit()

    logging.write_log(
        event_type=u"create_route_definition",
        event_severity=u"INFO",
        event=f"'{name}' route definition created."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition created."
    }


@handle_exception
def update_route_definition_func(route_definition_id, form):
    # Define variables
    name = form.name.data.title()
    description = form.description.data.capitalize()
    team_id = form.team.data
    status = form.status.data

    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    route_definition_object = route_definition["data"][0]

    if name != route_definition_object.name:
        route_definition_object.name = name

    if description != route_definition_object.description:
        route_definition_object.description = description

    if team_id != route_definition_object.team_id:
        route_definition_object.team_id = team_id

    if status is not route_definition_object.status:
        route_definition_object.status = status

    db.session.commit()

    logging.write_log(
        event_type=u"update_route_definition",
        event_severity=u"INFO",
        event=f"'{name}' route definition updated."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition updated."
    }


@handle_exception
def remove_route_definition_func(route_definition_id):
    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    route_definition_object = route_definition["data"][0]

    if route_definition_object.rules or route_definition_object.notification_integrations:
        raise DependencyError("error", "Route definition has rules. Delete rules before this operation.")

    db.session.delete(route_definition_object)
    db.session.commit()

    logging.write_log(
        event_type=u"remove_route_definition",
        event_severity=u"INFO",
        event=f"'{route_definition_object.name}' route definition removed."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition removed."
    }


@handle_exception
def create_route_definition_rule_func(route_definition_id, form):
    # Define variables
    column = form.column.data.lower()
    condition_not = form.condition_not.data.lower()
    condition = form.condition.data.lower()
    value = form.value.data

    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    route_definition_object = route_definition["data"][0]

    route_definition_object.rules.append(
        Rules(
            column=column,
            condition_not=condition_not,
            condition=condition,
            value=value
        )
    )

    db.session.commit()

    logging.write_log(
        event_type=u"create_route_definition_rule",
        event_severity=u"INFO",
        event=f"Rule added to '{route_definition_object.name}' route definition updated."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition rule added."
    }


@handle_exception
def remove_route_definition_rule_func(route_definition_id, rule_id):
    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)
    rule_definition = Rules.query.filter_by(id=rule_id).first()

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    if not rule_definition:
        raise ItemNotFoundError("error", "Rule not found.")

    route_definition_object = route_definition["data"][0]

    route_definition_object.rules.remove(
        rule_definition
    )

    db.session.delete(rule_definition)
    db.session.commit()

    logging.write_log(
        event_type=u"remove_route_definition_rule",
        event_severity=u"INFO",
        event=f"'{route_definition_object.name}' route definition rule removed."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition rule removed."
    }


@handle_exception
def create_route_definition_notification_integration_func(route_definition_id, form):
    # Define variables
    integration = get_all_integrations_func(integration_id=form.integration.data, as_object=True)
    responsible = form.responsible.data
    delay = form.delay.data

    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    if not integration["data"]:
        raise ItemNotFoundError("error", "Integration not found.")

    route_definition_object = route_definition["data"][0]
    integration_object = integration["data"][0]

    route_definition_object.notification_integrations.append(
        NotificationIntegrations(
            integration_id=integration_object.id,
            responsible=responsible,
            delay=delay
        )
    )
    db.session.commit()

    logging.write_log(
        event_type=u"create_route_definition_notification_rule",
        event_severity=u"INFO",
        event=f"'{route_definition_object.name}' route definition notification rule created."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition notification rule created."
    }


@handle_exception
def remove_route_definition_notification_integration_func(route_definition_id, rule_id):
    route_definition = get_all_route_definitions_func(route_definition_id=route_definition_id, as_object=True)
    rule_definition = NotificationIntegrations.query.filter_by(id=rule_id).first()

    if not route_definition["data"]:
        raise ItemNotFoundError("error", "Route definition not found.")

    if not rule_definition:
        raise ItemNotFoundError("error", "Notification rule not found.")

    route_definition_object = route_definition["data"][0]

    route_definition_object.notification_integrations.remove(
        rule_definition
    )

    db.session.delete(rule_definition)
    db.session.commit()

    logging.write_log(
        event_type=u"remove_route_definition_notification_rule",
        event_severity=u"INFO",
        event=f"'{route_definition_object.name}' route definition notification rule removed."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Route definition notification rule removed."
    }
