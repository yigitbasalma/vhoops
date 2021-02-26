#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.mysql import NVARCHAR, LONGTEXT, TINYINT

from vhoops import db, Base


class Integrations(Base):
    __tablename__ = "integrations"

    name = db.Column(NVARCHAR(255), nullable=False, unique=True)
    identifier = db.Column(NVARCHAR(255), nullable=False, unique=True)
    icon_url = db.Column(NVARCHAR(1024), nullable=False)
    config = db.Column(LONGTEXT, nullable=False)
    fields = db.Column(LONGTEXT, nullable=False)
    # 1: Available, 0: Unavailable
    is_available = db.Column(TINYINT(1), default=1)

    def __init__(self, **kwargs):
        super(Integrations, self).__init__(**kwargs)

    def __repr__(self):
        return '<Integration %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        return data
