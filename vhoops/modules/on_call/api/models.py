#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey

from vhoops import db, Base


class OnCall(Base):
    __tablename__ = "oncall"

    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    team_id = db.Column(db.Integer, ForeignKey("teams.id"))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    user = db.relationship("Users", foreign_keys=[user_id], lazy="subquery")
    team = db.relationship("Teams", foreign_keys=[team_id], lazy="subquery")

    def __init__(self, **kwargs):
        super(OnCall, self).__init__(**kwargs)

    def __repr__(self):
        return '<OnCall %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        data["user"] = self.user.as_dict
        data["team"] = self.team.as_dict

        return data
