#!/usr/bin/python
# -*- coding: utf-8 -*-

from vhoops import db, Base


class CeleryJobLogs(Base):
    __tablename__ = "celery_job_logs"

    name = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(255), unique=True)

    def __init__(self, **kwargs):
        super(CeleryJobLogs, self).__init__(**kwargs)

    def __repr__(self):
        return '<CeleryJobLog %r>' % self.id


db.create_all()
