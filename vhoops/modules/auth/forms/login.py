#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, BooleanField, validators
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [
            validators.DataRequired(),
        ],
        render_kw={
            'placeholder': 'root',
            'class': 'form-control',
            'aria-describedby': 'username',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    password = PasswordField(
        'Password',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': '************',
            'class': 'form-control form-control-merge',
            'aria-describedby': 'password',
            'tabindex': '2'
        }
    )
    remember_me = BooleanField(
        "Remember me?",
        render_kw={
            'class': 'custom-control-label',
            'tabindex': '3',
        },
        default=False
    )
