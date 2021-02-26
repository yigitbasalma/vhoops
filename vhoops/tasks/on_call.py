#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from datetime import datetime, timedelta
from flask_mail import Message

from vhoops import db, celery, email, email_template_base
from vhoops.external.x_tools import calculate_hash
from vhoops.modules.on_call.api.models import OnCall

from vhoops.tasks.celeryy.models import CeleryJobLogs

NOTIFY_BEFORE = 1  # Hours


@celery.task()
def notify_on_call_starts():
    notified_users = list()
    start_date = datetime.utcnow() - timedelta(hours=NOTIFY_BEFORE)

    try:
        on_call_users = OnCall.query.filter(
            OnCall.start.between(start_date, datetime.utcnow())
        ).all()

        email_template = open(os.path.join(email_template_base, "on-call-notify.html"), "r").read()

        if on_call_users:
            with email.connect() as e_conn:
                for user in on_call_users:
                    user_details = user.user
                    team_details = user.team

                    job_hash = calculate_hash(
                        f"{user_details.username} {user.start} {user.end} on_call_starts"
                    )

                    job_record = CeleryJobLogs.query.filter_by(hash=job_hash).first()
                    if job_record:
                        continue

                    message = Message(
                        html=email_template
                        .replace("$Firstname", user_details.first_name)
                        .replace("$Lastname", user_details.last_name)
                        .replace("$Message", f"Your duty begins within {NOTIFY_BEFORE} hour!"),
                        recipients=[user_details.email],
                        subject="On Call Duty Begin Reminder."
                    )
                    e_conn.send(message)

                    db.session.add(
                        CeleryJobLogs(
                            name="notify_on_call_starts",
                            hash=job_hash
                        )
                    )
                    db.session.commit()

                    notified_users.append(dict(
                        username=user_details.username,
                        email=user_details.email,
                        team=team_details.name
                    ))
    except Exception as e:
        print(str(e))

    return {
        "data": notified_users
    }


@celery.task()
def notify_on_call_ends():
    notified_users = list()
    end_date = datetime.utcnow() - timedelta(hours=NOTIFY_BEFORE)

    try:
        on_call_users = OnCall.query.filter(
            OnCall.end.between(end_date, datetime.utcnow())
        ).all()

        email_template = open(os.path.join(email_template_base, "on-call-notify.html"), "r").read()

        if on_call_users:
            with email.connect() as e_conn:
                for user in on_call_users:
                    user_details = user.user
                    team_details = user.team

                    job_hash = calculate_hash(
                        f"{user_details.username} {user.start} {user.end} on_call_end"
                    )

                    job_record = CeleryJobLogs.query.filter_by(hash=job_hash).first()
                    if job_record:
                        continue

                    message = Message(
                        html=email_template
                        .replace("$Firstname", user_details.first_name)
                        .replace("$Lastname", user_details.last_name)
                        .replace("$Message", f"Your duty ends within {NOTIFY_BEFORE} hour!"),
                        recipients=[user_details.email],
                        subject="On Call Duty Ends Reminder."
                    )
                    e_conn.send(message)

                    db.session.add(
                        CeleryJobLogs(
                            name="notify_on_call_ends",
                            hash=job_hash
                        )
                    )
                    db.session.commit()

                    notified_users.append(dict(
                        username=user_details.username,
                        email=user_details.email,
                        team=team_details.name
                    ))
    except Exception as e:
        print(str(e))

    return {
        "data": notified_users
    }
