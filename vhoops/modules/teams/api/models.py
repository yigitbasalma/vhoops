#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.mysql import NVARCHAR

from vhoops import db, Base

TeamMember = db.Table(
    'team_members', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
)


class Teams(Base):
    __tablename__ = "teams"

    name = db.Column(NVARCHAR(64), nullable=False)
    description = db.Column(NVARCHAR(255), nullable=False)

    members = db.relationship("Users", secondary=TeamMember)

    def __init__(self, **kwargs):
        super(Teams, self).__init__(**kwargs)

    def __repr__(self):
        return '<Team %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))
        return data
