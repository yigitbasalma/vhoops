#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import desc, and_
from flask_login import current_user

from vhoops import db, logging
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import ItemNotFoundError, ResourceError, ConditionError
from vhoops.external.x_tools import calculate_hash, get_future_date, calculate_elapsed

from vhoops.modules.alerts.api.models import Alerts, Actions, Comments


@handle_exception
def mark_as_seen_func(alert):
    action_hash = calculate_hash(f"'{current_user.username}' '{alert.id}' seen-alert")

    if Actions.query.filter_by(hash=action_hash).first():
        return

    action = Actions(
        details=f"'{current_user.username}' seen alert.",
        hash=action_hash
    )
    alert.actions.append(action)

    if not alert.is_seen:
        alert.is_seen = True
        alert.updated_at = db.func.current_timestamp()

    db.session.commit()

    logging.write_log(
        event_type=u"seen_alert",
        event_severity=u"INFO",
        event=f"'{current_user.username}' seen alert."
    )


@handle_exception
def get_alerts_func(alert_id=None, as_object=False, filters=None):
    query = Alerts.query
    query_filters = list()

    available_filters = {
        "status": {
            "all": [Alerts.status.in_(("open", "closed", "ack"))]
        }
    }

    if alert_id:
        query_filters.append(
            Alerts.id == alert_id
        )

    if not current_user.has_group("superuser"):
        query_filters.append(
            Alerts.team_id.in_([i.id for i in current_user.teams])
        )

    if filters:
        for _filter in filters.split(","):
            filter_name, filter_value = _filter.split(":")
            query_filters.append(
                available_filters[filter_name][filter_value][0]
                if available_filters.get(filter_name, dict()).get(filter_value)
                else getattr(Alerts, filter_name) == filter_value
            )

    return {
        "data": [
            i.as_dict if not as_object else i
            for i in query.filter(and_(*query_filters)).order_by(desc(Alerts.registration_timestamp)).all()
        ]
    }


@handle_exception
def create_new_alert_func(form):
    alert = Alerts.query.filter_by(alias=form.alias.data).first()

    if alert:
        alert.alert_count += 1
        alert.last_occurred_at = db.func.current_timestamp()
        db.session.commit()

        logging.write_log(
            event_type=u"api_create_alert",
            event_severity=u"INFO",
            event=f"'{form.alias.data}' alert occurred {alert.alert_count} times."
        )
    else:
        db.session.add(
            Alerts(
                alias=form.alias.data.title(),
                message=form.message.data.capitalize(),
                tags=form.tags.data if not isinstance(form.tags.data, (list, tuple)) else ",".join(form.tags.data),
                source=form.source.data.title(),
                priority=form.priority.data.upper(),
                team_id=current_user.teams[0].id
            )
        )
        db.session.commit()

        logging.write_log(
            event_type=u"create_alert",
            event_severity=u"INFO",
            event=f"'{form.alias.data}' alert created."
        )

    return {
        "status": "success",
        "refresh": True,
        "message": "Alert created."
    }


@handle_exception
def create_comment_for_alert_func(form, alert_id):
    alert = get_alerts_func(alert_id=alert_id, as_object=True)

    if not alert["data"]:
        raise ItemNotFoundError("error", "Alert not found.")

    alert_object = alert["data"][0]
    comment = Comments(
        comment=form.comment.data.capitalize(),
        user_id=current_user.id
    )

    alert_object.comments.append(comment)

    db.session.commit()

    logging.write_log(
        event_type=u"create_alert_comment",
        event_severity=u"INFO",
        event=f"Comment created for '{alert_object.alias}'."
    )

    return {
        "status": "success",
        "refresh": True,
        "message": "Comment created."
    }


@handle_exception
def change_ack_status_func(alert_id, state):
    alert = get_alerts_func(alert_id=alert_id, as_object=True)

    if not alert["data"]:
        raise ItemNotFoundError("error", "Alert not found.")

    alert_object = alert["data"][0]

    if alert_object.status == "closed":
        raise ConditionError("error", "You cannot change status for closed alerts.")

    # TODO: Make celery job for control
    if state == "ack":
        if not alert_object.snoozed:
            action_hash = calculate_hash(f"'{current_user.username}' '{alert_object.id}' ack-alert")

            alert_object.status = "ack"
            alert_object.snoozed = True
            alert_object.snoozed_until = get_future_date(days=1)

            if not Actions.query.filter_by(hash=action_hash).first():
                alert_object.actions.append(
                    Actions(
                        details=f"'{current_user.username}' ack alert.",
                        hash=action_hash
                    )
                )

            logging.write_log(
                event_type=u"alert_acknowledged",
                event_severity=u"INFO",
                event=f"Alert acknowledged '{alert_object.alias}'."
            )
    elif state == "un-ack":
        if alert_object.snoozed:
            action_hash = calculate_hash(f"'{current_user.username}' '{alert_object.id}' un-ack-alert")

            alert_object.status = "open"
            alert_object.snoozed = False
            alert_object.snoozed_until = None

            if not Actions.query.filter_by(hash=action_hash).first():
                alert_object.actions.append(
                    Actions(
                        details=f"'{current_user.username}' un-ack alert.",
                        hash=action_hash
                    )
                )

            logging.write_log(
                event_type=u"alert_un_acknowledged",
                event_severity=u"INFO",
                event=f"Alert un-acknowledged '{alert_object.alias}'."
            )
    else:
        raise ResourceError("error", "Unknown state.")

    db.session.commit()

    return {
        "status": "success",
        "refresh": True,
        "message": "Acknowledge status changed."
    }


@handle_exception
def close_alert_func(alert_id):
    alert = get_alerts_func(alert_id=alert_id, as_object=True)

    if not alert["data"]:
        raise ItemNotFoundError("error", "Alert not found.")

    alert_object = alert["data"][0]

    if alert_object.status not in ("closed", ):
        action_hash = calculate_hash(f"'{current_user.username}' '{alert_object.id}' close-alert")
        elapsed_for_resolve = calculate_elapsed(alert_object.registration_timestamp, formatted=True)
        report = f"{current_user.username}={elapsed_for_resolve}"

        alert_object.status = "closed"
        alert_object.updated_at = db.func.current_timestamp()
        alert_object.report = report
        alert_object.snoozed = False
        alert_object.snoozed_until = None

        if not Actions.query.filter_by(hash=action_hash).first():
            alert_object.actions.append(
                Actions(
                    details=f"'{current_user.username}' close alert.",
                    hash=action_hash
                )
            )

        db.session.commit()

        logging.write_log(
            event_type=u"alert_closed",
            event_severity=u"INFO",
            event=f"Alert closed '{alert_object.alias}'."
        )

    return {
        "status": "success",
        "refresh": True,
        "message": "Alert closed."
    }
