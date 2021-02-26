#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, not_

from vhoops import app_cache
from vhoops.wrappers.exceptions import handle_exception
from vhoops.external.x_exceptions import ItemNotFoundError
from vhoops.external.x_tools import make_dict_sqlalchemy

from vhoops.modules.alerts.api.models import Alerts


@handle_exception
def analytics_api_func(module_name, request_args):
    modules = dict(
        alerts=Alerts
    )
    operators = dict(
        equal=lambda *args: getattr(module, args[0]) == args[1],
        not_equal=lambda *args: getattr(module, args[0]) != args[1],
        greater_than=lambda *args: getattr(module, args[0]) > args[1],
        lower_than=lambda *args: getattr(module, args[0]) < args[1],
        contains=lambda *args: getattr(module, args[0]).contains(args[1]),
        not_contains=lambda *args: not_(getattr(module, args[0]).contains(args[1])),
        between=lambda *args: getattr(module, args[0]).between(args[1], args[2])
    )
    result_operators = dict(
        first=lambda q, f: dict(data=[make_dict_sqlalchemy(q.filter(and_(*f)).first(), module)]),
        all=lambda q, f: dict(data=[make_dict_sqlalchemy(i, module) for i in q.filter(and_(*f)).all()]),
        count=lambda q, f: dict(count=q.filter(and_(*f)).count())
    )

    if not modules.get(module_name):
        raise ItemNotFoundError("error", "Requested module not found.")

    module = modules[module_name]
    query = module.query
    query_filters = module.base_filters(module)
    with_entities = list()
    result_operator = request_args.get("return", "alert_count")

    for _filter in request_args.get("filters", "").split(";"):
        filter_pack = _filter.split("|")
        # For pop operator from filter pack
        filter_pack.reverse()
        operator = filter_pack.pop()
        # Reverse again for correct parse in lambda
        filter_pack.reverse()
        query_filters.append(
            operators[operator](*filter_pack)
        )

    if request_args.get("columns"):
        for _column in request_args.get("columns", "").split(","):
            with_entities.append(_column)

        query = query.with_entities(*with_entities)

    return result_operators[result_operator](query, query_filters)


@handle_exception
def downtime_info_func():
    cached_data = app_cache.read_key(
        bucket="app_cache",
        cache_key="downtime_calculator",
        prefix="downtime_calculator"
    )

    if not cached_data:
        return dict(data=list())

    data = list()

    for short_date, d_data in cached_data.items():
        total_downtime = 0
        for d_info in d_data:
            total_downtime += d_info["down_time"]
        data.append(dict(
            # Just date
            date=short_date,
            downtime=total_downtime
        ))

    return dict(
        data=data
    )
