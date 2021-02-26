#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import hashlib
import datetime
import string
import json

from random import randint, choice


def strong_password():
    characters = string.ascii_letters + string.digits + "_*!."
    return "".join(choice(characters) for _ in range(randint(8, 16)))


def generate_id():
    return str(uuid.uuid4()).lower().split("-")[-1]


def generate_token():
    return str(uuid.uuid4())


def calculate_hash(target, method="sha256"):
    method_dict = {
        "md5": hashlib.md5,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    return method_dict[method](target.encode("utf-8")).hexdigest()


def datetime_pattern(pt=None, dt=None, ct=None, skip_format=False):
    pattern_dict = {
        "ts": "%d/%m/%Y-%H:%M:%S",
        "date": "%Y-%m-%d",
        "js": "%Y-%m-%d %H:%M",
        "copyrights": "%Y"
    }
    now = datetime.datetime.utcnow()
    if pt is None:
        pt = "ts"
    if dt is not None:
        if ct is None:
            return dt.strftime(pattern_dict[pt])
        return datetime.datetime.strptime(dt, pattern_dict[ct]).strftime(pattern_dict[pt])
    return now.strftime(pattern_dict[pt]) if not skip_format else now


def get_future_date(days):
    return datetime.datetime.now() + datetime.timedelta(days=days)


def calculate_elapsed(time_object, formatted=False):
    if formatted:
        return str((datetime.datetime.now() - time_object))
    return (datetime.datetime.now() - time_object).total_seconds()


def pretty_json(data, indent=4):
    return json.dumps(json.loads(data), indent=indent)


def make_dict_sqlalchemy(result_object, table):
    result_dict = dict()
    for c_name in table.__table__.columns:
        if hasattr(result_object, c_name.key):
            result_dict[c_name.key] = str(getattr(result_object, c_name.key))

    return result_dict
