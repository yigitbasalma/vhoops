#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps

from flask import request, jsonify, current_app
from flask_login import login_user, current_user

from vhoops.modules.auth.api.models import Users


def mixed_login(f):
    # noinspection PyBroadException
    @wraps(f)
    def decorator(*args, **kwargs):
        is_api = False

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            is_api = True

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                user = Users.query.filter_by(password=token).first()
                if not user:
                    raise TypeError
                login_user(user)
            except TypeError:
                return jsonify({'message': 'token is invalid'})
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        return f(is_api, *args, **kwargs)
    return decorator
