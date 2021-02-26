#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.mysql import NVARCHAR, TINYINT, LONGTEXT
from sqlalchemy import ForeignKey, UniqueConstraint

from vhoops import db, Base


RoutingRules = db.Table(
    'routing_rules', db.Model.metadata,
    db.Column('definition_id', db.Integer, db.ForeignKey('route_definitions.id')),
    db.Column('rule_id', db.Integer, db.ForeignKey('rule_definitions.id'))
)

NotificationRules = db.Table(
    'notification_rules', db.Model.metadata,
    db.Column('definition_id', db.Integer, db.ForeignKey('route_definitions.id')),
    db.Column('rule_id', db.Integer, db.ForeignKey('notification_integration_definitions.id'))
)


class Routes(Base):
    __tablename__ = "route_definitions"

    name = db.Column(NVARCHAR(255), nullable=False)
    description = db.Column(LONGTEXT, nullable=False)
    team_id = db.Column(db.Integer, ForeignKey("teams.id"))
    # 1: Available, 0: Unavailable
    status = db.Column(TINYINT(1), default=1)

    rules = db.relationship("Rules", secondary=RoutingRules)
    notification_integrations = db.relationship("NotificationIntegrations", secondary=NotificationRules)
    team = db.relationship("Teams", foreign_keys=[team_id], lazy="subquery")

    UniqueConstraint(name, team_id)

    def __init__(self, **kwargs):
        super(Routes, self).__init__(**kwargs)

    def __repr__(self):
        return '<Route %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        data["team"] = self.team.as_dict

        return data


class Rules(Base):
    __tablename__ = "rule_definitions"

    column = db.Column(NVARCHAR(255), nullable=False)
    condition = db.Column(NVARCHAR(64), nullable=False)
    # 1: Condition, 0: Not Condition
    condition_not = db.Column(TINYINT(1), default=1)
    value = db.Column(LONGTEXT, nullable=False)

    def __init__(self, **kwargs):
        super(Rules, self).__init__(**kwargs)

    def __repr__(self):
        return '<Rule %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        return data


class NotificationIntegrations(Base):
    __tablename__ = "notification_integration_definitions"

    integration_id = db.Column(db.Integer, ForeignKey("integrations.id"))
    # 1: Team, 0: On-Call user
    responsible = db.Column(TINYINT(1), default=0)
    delay = db.Column(db.Integer, default=0)
    extra_parameters = db.Column(LONGTEXT)

    integration = db.relationship("Integrations", foreign_keys=[integration_id], lazy="subquery")

    def __init__(self, **kwargs):
        super(NotificationIntegrations, self).__init__(**kwargs)

    def __repr__(self):
        return '<NotificationIntegration %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        data["integration"] = self.integration.as_dict

        return data
