#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import SelectField, DateTimeField, validators
from flask_wtf import FlaskForm


class NewOnCallSchedule(FlaskForm):
    user = SelectField(
        'Username',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Username',
            'class': 'form-control users',
            'id': 'username'
        }
    )
    start_date = DateTimeField(
        'Start Date',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Start date',
            'class': 'form-control',
            'id': 'start_date'
        },
        format="%Y-%m-%d %H:%M"
    )
    end_date = DateTimeField(
        'End date',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'End Date',
            'class': 'form-control',
            'id': 'end_date'
        },
        format="%Y-%m-%d %H:%M"
    )
