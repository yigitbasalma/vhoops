#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import amqp

from sqlalchemy import and_
from datetime import datetime, timedelta

from vhoops import db, celery
from vhoops.external.x_tools import calculate_hash
from vhoops.modules.routing_rules.api.models import Routes
from vhoops.modules.alerts.api.models import Alerts
from vhoops.modules.on_call.api.models import OnCall
from vhoops.modules.alerts.api.models import Actions

from vhoops.tasks.celeryy.models import CeleryJobLogs


# noinspection PyBroadException
@celery.task()
def configure_routing():
    # Get all route definitions
    route_definitions = Routes.query.filter_by(status=True).all()

    with amqp.Connection(**celery.conf.get("amqp_config")) as rabbit:
        # Create channel
        ch = rabbit.channel()
        for route in route_definitions:
            try:
                # Build filter for alert query
                query_filters = [
                    Alerts.team_id == route.team_id,
                    Alerts.status != "closed"
                ]
                for rule in route.rules:
                    query_filters.extend(
                        getattr(Alerts, rule.condition)(
                            Alerts,
                            column=rule.column,
                            condition_not=rule.condition_not,
                            value=rule.value
                        )
                    )

                # Get On Call list for team
                on_call_users = OnCall.query.filter(
                    and_(
                        OnCall.team_id == route.team_id,
                        OnCall.end >= (datetime.utcnow() - timedelta(minutes=10))
                    )
                ).all()

                # Get all alerts with filters
                alerts = Alerts.query.filter(and_(*query_filters)).all()
                for alert in alerts:
                    alert_definition = dict(
                        alert=alert.as_notification_dict,
                        responders=[i.user.as_notification_dict for i in on_call_users],
                        extra_parameters=list()
                    )

                    for n_rule in route.notification_integrations:
                        # Create job hash
                        job_hash = calculate_hash(
                            f"{n_rule.id} {n_rule.delay} {alert.id} {alert.alert_count} {alert.alias} "
                            f"{alert.registration_timestamp} configure_routing"
                        )

                        # If exactly same alert, continue
                        job_record = CeleryJobLogs.query.filter_by(hash=job_hash).first()
                        if job_record:
                            continue

                        # Check for delay option
                        if n_rule.delay:
                            if not (alert.registration_timestamp <
                                    (datetime.utcnow() + timedelta(seconds=n_rule.delay))):
                                continue

                        # Check for who is the responsible
                        # Team responsible if n_rule.responsible is True else on call user
                        if n_rule.responsible:
                            alert_definition["responders"] = [on_call_users.team.as_notification_dict]

                        if n_rule.extra_parameters:
                            alert_definition["extra_parameters"] = json.loads(n_rule.extra_parameters)

                        ch.basic_publish(
                            amqp.Message(json.dumps(alert_definition)),
                            routing_key=n_rule.integration.identifier
                        )

                        db.session.add(
                            CeleryJobLogs(
                                name="configure_routing",
                                hash=job_hash
                            )
                        )

                        db.session.commit()

                        action_hash = calculate_hash(
                            f"{n_rule.id} {n_rule.delay} {alert.id} {alert.alert_count} {alert.alias} "
                            f"{alert.registration_timestamp} notification-sent")

                        if Actions.query.filter_by(hash=action_hash).first():
                            return

                        action = Actions(
                            details=f"Alert sent to '{alert_definition['responders']}'.",
                            hash=action_hash
                        )
                        alert.actions.append(action)

                        db.session.commit()
            except Exception as e:
                print(str(e))
                continue
