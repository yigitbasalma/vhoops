#!/usr/bin/python
# -*- coding: utf-8 -*-

imports = [
    "vhoops.tasks.on_call",
    "vhoops.tasks.alert_routing",
    "vhoops.tasks.calculate_downtime"
]
timezone = "UTC"

accept_content = ["json", "msgpack", "yaml"]
result_serializer = "json"

result_backend = "redis://192.168.56.2:6379/1"

beat_schedule = {
    "on-call-start": {
        "task": "vhoops.tasks.on_call.notify_on_call_starts",
        "schedule": 30.0,
    },
    "on-call-end": {
        "task": "vhoops.tasks.on_call.notify_on_call_ends",
        "schedule": 30.0,
    },
    "alert-routing": {
        "task": "vhoops.tasks.alert_routing.configure_routing",
        "schedule": 10.0,
    },
    "downtime-calculate": {
        "task": "vhoops.tasks.calculate_downtime.calculate",
        "schedule": 30.0
    }
}

amqp_config = dict(
    host="192.168.56.3:5672",
    userid="admin",
    password="admin",
    hearbeat=30
)
