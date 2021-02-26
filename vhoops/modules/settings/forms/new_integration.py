#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, TextAreaField, BooleanField, validators
from flask_wtf import FlaskForm

from vhoops.external.x_tools import pretty_json


class NewIntegration(FlaskForm):
    name = StringField(
        'Integration Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=255)
        ],
        render_kw={
            'placeholder': 'Slack',
            'class': 'form-control'
        }
    )
    identifier = StringField(
        'Identifier',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=255),
            validators.Regexp("^[a-z_]+$")
        ],
        render_kw={
            'placeholder': 'slack_integration',
            'class': 'form-control'
        }
    )
    integration_icon = StringField(
        'Integration Icon',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=1024)
        ],
        render_kw={
            'placeholder': 'https://assets.stickpng.com/images/5cb480cd5f1b6d3fbadece79.png',
            'class': 'form-control'
        }
    )
    config = TextAreaField(
        'Integration Json',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=2048)
        ],
        render_kw={
            'placeholder': pretty_json(
                '{"token": "asdASD123", "username": "alertost", "icon_emoji": ":robot_face:"}',
                indent=4
            ),
            'class': 'form-control',
            'rows': '5'
        }
    )
    fields = TextAreaField(
        'Required Fields Json',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=2048)
        ],
        render_kw={
            'placeholder': pretty_json(
                '{"to": "$To", "subject": "$Subject", "message": "$Message"}',
                indent=4
            ),
            'class': 'form-control',
            'rows': '5'
        }
    )
    is_available = BooleanField(
        "Is available?",
        [
            validators.AnyOf([True, False])
        ],
        render_kw={
            'class': 'custom-control-input',
            'id': 'is-available'
        },
        default=True
    )
