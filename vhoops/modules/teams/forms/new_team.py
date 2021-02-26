#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, TextAreaField, validators
from flask_wtf import FlaskForm


class NewTeam(FlaskForm):
    name = StringField(
        'Team Name',
        [
            validators.DataRequired(),
            validators.Length(min=6, max=35)
        ],
        render_kw={
            'placeholder': 'SRE_Team',
            'class': 'form-control dt-team-name',
            'aria-label': 'SRE_Team'
        }
    )
    description = TextAreaField(
        'Description',
        [
            validators.DataRequired(),
            validators.Length(min=6, max=255)
        ],
        render_kw={
            'placeholder': 'Team descriptions ....',
            'class': 'form-control dt-team-description',
            'aria-label': 'Team descriptions ....'
        }
    )
