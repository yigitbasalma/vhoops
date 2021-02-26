#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_

from vhoops import celery, app_cache
from vhoops.modules.alerts.api.models import Alerts


@celery.task()
def calculate():
    key_tag = "possible-downtime"
    downtimes = dict()

    try:
        alerts = Alerts.query.with_entities(
            Alerts.registration_timestamp,
            Alerts.updated_at
        ).filter(and_(
            Alerts.status == "closed",
            Alerts.tags.contains(key_tag)
        )).all()

        for alert in alerts:
            short_date = str(alert.registration_timestamp).split()[0]
            if downtimes.get(short_date):
                downtimes[short_date].append(dict(
                    start_time=str(alert.registration_timestamp),
                    end_time=str(alert.updated_at),
                    down_time=(alert.updated_at - alert.registration_timestamp).total_seconds()
                ))
                continue

            downtimes[short_date] = [dict(
                start_time=str(alert.registration_timestamp),
                end_time=str(alert.updated_at),
                down_time=(alert.updated_at - alert.registration_timestamp).total_seconds()
            )]

        app_cache.write_key(
            bucket="app_cache",
            cache_key="downtime_calculator",
            cache_value=downtimes,
            prefix="downtime_calculator",
            ttl=86400
        )
    except Exception as e:
        print(str(e))
