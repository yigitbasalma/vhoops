#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import TextAreaField, validators
from flask_wtf import FlaskForm


class NewComment(FlaskForm):
    comment = TextAreaField(
        'Comment',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=2048)
        ],
        render_kw={
            'placeholder': 'Comment',
            'class': 'form-control mb-2'
        }
    )