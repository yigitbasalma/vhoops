#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

from vhoops import api_version
from vhoops.wrappers.mixed_login import mixed_login

from vhoops.modules.analytics.api.controllers import analytics_api_func, downtime_info_func

analytics_router_api = Blueprint("analytics_router_api", __name__, url_prefix=api_version + "/analytics")


@analytics_router_api.route("/<module_name>", methods=["GET"])
@mixed_login
def analytics_api(_, module_name):
    return jsonify(
        analytics_api_func(module_name=module_name, request_args=request.args)
    )


@analytics_router_api.route("/downtime", methods=["GET"])
@mixed_login
def downtime_analytics_api(_):
    return jsonify(
        downtime_info_func()
    )
