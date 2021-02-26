#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, SelectMultipleField, SelectField, validators
from flask_wtf import FlaskForm


class NewUser(FlaskForm):
    first_name = StringField(
        'First Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=35)
        ],
        render_kw={
            'placeholder': 'First name',
            'class': 'form-control'
        }
    )
    last_name = StringField(
        'Last Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=35)
        ],
        render_kw={
            'placeholder': 'Last name',
            'class': 'form-control'
        }
    )
    username = StringField(
        'Username',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=35)
        ],
        render_kw={
            'placeholder': 'Last name',
            'class': 'form-control'
        }
    )
    email = StringField(
        'Email',
        [
            validators.DataRequired(),
            validators.Email()
        ],
        render_kw={
            'placeholder': 'Email',
            'class': 'form-control'
        }
    )
    phone = StringField(
        'Phone Number',
        [
            validators.DataRequired(),
            validators.Regexp(regex="^[5][0-9 ]{12}$")
        ],
        render_kw={
            'placeholder': 'Phone number',
            'class': 'form-control phone-number'
        }
    )
    teams = SelectMultipleField(
        'Teams',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Teams',
            'class': 'team-name'
        },
        choices=list()
    )
    group = SelectField(
        'Group',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Group',
            'class': 'group-name'
        },
        choices=list()
    )
