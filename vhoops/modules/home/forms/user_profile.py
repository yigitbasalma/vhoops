#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, validators
from flask_wtf import FlaskForm


class General(FlaskForm):
    first_name = StringField(
        'First Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=35)
        ],
        render_kw={
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
            'class': 'form-control phone-number'
        }
    )


class ChangePassword(FlaskForm):
    old_password = PasswordField(
        'Old Password',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Old Password',
            'class': 'form-control',
            'id': 'account-old-password'
        }
    )
    new_password = PasswordField(
        'New Password',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'New Password',
            'class': 'form-control',
            'id': 'account-new-password'
        }
    )
    retype_new_password = PasswordField(
        'Retype New Password',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': 'Retype New Password',
            'class': 'form-control',
            'id': 'account-retype-new-password'
        }
    )
