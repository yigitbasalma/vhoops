#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, desc

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import ItemNotFoundError

from vhoops.modules.settings.api.models import Integrations


@handle_exception
def get_all_integrations_func(integration_id=None, as_object=False):
    query = Integrations.query
    query_filters = list()

    if integration_id:
        query_filters.append(
            Integrations.id == integration_id
        )

    return {
        "data": [
            i.as_dict if not as_object else i
            for i in query.filter(and_(*query_filters)).order_by(desc(Integrations.registration_timestamp)).all()
        ]
    }


@handle_exception
def create_new_integration_func(form):
    db.session.add(
        Integrations(
            name=form.name.data.title(),
            identifier=form.identifier.data.lower(),
            icon_url=form.integration_icon.data,
            config=form.config.data,
            fields=form.fields.data
        )
    )
    db.session.commit()

    logging.write_log(
        event_type=u"create_integration",
        event_severity=u"INFO",
        event=f"'{form.name.data}' integration created."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Integration created."
    }


@handle_exception
def update_integration_func(form, integration_id):
    # Define variables
    integration_name = form.name.data.title()
    icon_url = form.integration_icon.data
    config = form.config.data
    fields = form.fields.data
    is_available = form.is_available.data

    integration = get_all_integrations_func(integration_id=integration_id, as_object=True)

    if not integration["data"]:
        raise ItemNotFoundError("error", "Integration not found.")

    integration_object = integration["data"][0]

    if integration_name != integration_object.name:
        integration_object.name = integration_name

    if icon_url != integration_object.icon_url:
        integration_object.icon_url = icon_url

    if config != integration_object.config:
        integration_object.config = config

    if fields != integration_object.fields:
        integration_object.fields = fields

    if is_available is not integration_object.is_available:
        integration_object.is_available = is_available

    db.session.commit()

    logging.write_log(
        event_type=u"update_integration",
        event_severity=u"INFO",
        event=f"'{integration_name}' integration edited."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Integration edited."
    }
