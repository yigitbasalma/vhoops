#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm

from vhoops import alert_priorities


class NewAlert(FlaskForm):
    alias = StringField(
        'Alias',
        [
            validators.DataRequired(),
            validators.Length(min=6, max=255)
        ],
        render_kw={
            'placeholder': 'Alias',
            'class': 'form-control'
        }
    )
    message = TextAreaField(
        'Message',
        [
            validators.DataRequired(),
            validators.Length(min=5, max=2048)
        ],
        render_kw={
            'placeholder': 'Message',
            'class': 'form-control'
        }
    )
    source = TextAreaField(
        'Source',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=255)
        ],
        render_kw={
            'placeholder': 'Source',
            'class': 'form-control'
        }
    )
    priority = SelectField(
        'Priority',
        [
            validators.DataRequired(),
            validators.AnyOf(alert_priorities.keys())
        ],
        render_kw={
            'placeholder': 'Source',
            'class': 'form-control'
        },
        choices=alert_priorities.keys()
    )
    tags = StringField(
        'Tags',
        [
            validators.Length(min=0, max=1024)
        ],
        render_kw={
            'placeholder': 'Tags',
            'class': 'form-control'
        }
    )
