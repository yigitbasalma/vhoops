#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, SelectField, TextAreaField, BooleanField, validators
from flask_wtf import FlaskForm

from vhoops import routing_rules_conditions
from vhoops.external.x_tools import pretty_json


class RouteDefinition(FlaskForm):
    name = StringField(
        'Route Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=255)
        ],
        render_kw={
            'placeholder': 'All alert',
            'class': 'form-control'
        }
    )
    description = TextAreaField(
        'Description',
        [
            validators.DataRequired(),
            validators.Length(min=6, max=2048)
        ],
        render_kw={
            'placeholder': 'Route descriptions ....',
            'class': 'form-control'
        }
    )
    team = SelectField(
        'Team',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Group',
            'class': 'team-name'
        }
    )
    status = BooleanField(
        "Is Active?",
        [
            validators.AnyOf([True, False])
        ],
        render_kw={
            'class': 'custom-control-input',
            'id': 'is-available'
        },
        default=True
    )


class RuleDefinition(FlaskForm):
    column = SelectField(
        'Column',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Column',
            'class': 'column-name'
        }
    )
    condition_not = SelectField(
        'Condition Not',
        [
            validators.DataRequired(),
            validators.AnyOf(["1", "0"])
        ],
        render_kw={
            'placeholder': 'Column',
            'class': 'condition-not-name'
        },
        choices=[(1, "NOT"), (0, "-")]
    )
    condition = SelectField(
        'Condition',
        [
            validators.DataRequired(),
            validators.AnyOf([
                k
                for k in routing_rules_conditions.keys()
            ])
        ],
        render_kw={
            'placeholder': 'Column',
            'class': 'condition-name'
        },
        choices=[
            (k, v)
            for k, v in routing_rules_conditions.items()
        ]
    )
    value = StringField(
        'Value',
        [
            validators.DataRequired(),
            validators.Length(min=1, max=255)
        ],
        render_kw={
            'placeholder': 'Value',
            'class': 'form-control'
        }
    )


class NotificationIntegration(FlaskForm):
    integration = SelectField(
        'Integration',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Choose integration',
            'class': 'integration-name'
        }
    )
    responsible = SelectField(
        'Responsible',
        [
            validators.DataRequired(),
            validators.AnyOf(["1", "0"])
        ],
        render_kw={
            'placeholder': 'Who is responsible',
            'class': 'responsible-name'
        },
        choices=[(1, "Team"), (0, "On-Call User")]
    )
    delay = StringField(
        'Delay',
        [
            validators.DataRequired(),
            validators.Regexp("^[0-9]{1,5}$")
        ],
        render_kw={
            'placeholder': 'How long seconds wait before send notification',
            'class': 'form-control'
        }
    )
    extra_parameters = TextAreaField(
        'Extra Parameters',
        [
            validators.DataRequired(),
            validators.Length(min=6, max=2048)
        ],
        render_kw={
            'placeholder': pretty_json('{"config-key": "config-value"}'),
            'class': 'form-control',
            'rows': 5
        }
    )
