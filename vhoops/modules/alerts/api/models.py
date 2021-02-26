#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey, not_
from sqlalchemy.dialects.mysql import NVARCHAR, LONGTEXT, TINYINT

from vhoops import db, Base

AlertComments = db.Table(
    'alert_comments', db.Model.metadata,
    db.Column('alert_id', db.Integer, db.ForeignKey('alerts.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
)

AlertActions = db.Table(
    'alert_actions', db.Model.metadata,
    db.Column('alert_id', db.Integer, db.ForeignKey('alerts.id')),
    db.Column('action_id', db.Integer, db.ForeignKey('actions.id'))
)


class Alerts(Base):
    __tablename__ = "alerts"
    __searchables__ = [
        "alias", "message", "alert_count", "source", "priority"
    ]

    alias = db.Column(NVARCHAR(255), nullable=False)
    message = db.Column(LONGTEXT, nullable=False)
    # open, closed, ack
    status = db.Column(db.String(32), server_default="open")
    is_seen = db.Column(TINYINT(1), server_default="0")
    tags = db.Column(LONGTEXT)
    snoozed = db.Column(TINYINT(1), server_default="0")
    snoozed_until = db.Column(db.DateTime)
    alert_count = db.Column(db.Integer, server_default="1")
    last_occurred_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    source = db.Column(NVARCHAR(255), nullable=False)
    priority = db.Column(db.String(2))
    # resolve_time: <elapsed-sec>,closed_by: <username>
    report = db.Column(NVARCHAR(255))
    team_id = db.Column(db.Integer, ForeignKey("teams.id"))

    comments = db.relationship("Comments", secondary=AlertComments, order_by="desc(Comments.registration_timestamp)")
    actions = db.relationship("Actions", secondary=AlertActions, order_by="desc(Actions.registration_timestamp)")
    team = db.relationship("Teams", foreign_keys=[team_id])

    def __init__(self, **kwargs):
        super(Alerts, self).__init__(**kwargs)

    def __repr__(self):
        return '<Alert %r>' % self.id

    @property
    def as_notification_dict(self):
        return dict(
            id=self.id,
            alias=self.alias,
            message=self.message,
            count=self.alert_count,
            priority=self.priority
        )

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        data["comments"] = [i.as_dict for i in self.comments]
        data["actions"] = [i.as_dict for i in self.actions]
        data["team"] = self.team.as_dict

        return data

    @staticmethod
    def _not(condition_not, query):
        return not_(query) if condition_not else query

    def is_empty(self, column, condition_not, _):
        """Is empty filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column) is None
            )
        ]

    def regex_match(self, column, condition_not, value):
        """Regex filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column).contains(value)
            )
        ]

    def contains(self, column, condition_not, value):
        """Contains filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column).contains(value)
            )
        ]

    def starts_with(self, column, condition_not, value):
        """Starts with filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column).startswith(value)
            )
        ]

    def ends_with(self, column, condition_not, value):
        """Ends with filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column).endswith(value)
            )
        ]

    def eq(self, column, condition_not, value):
        """Equal filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column) == value
            )
        ]

    def gt(self, column, condition_not, value):
        """Greater than filter query"""
        return [
            self._not(
                condition_not=condition_not,
                query=getattr(self, column) < value
            )
        ]


class Comments(Base):
    __tablename__ = "comments"

    comment = db.Column(LONGTEXT, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    user = db.relationship("Users", foreign_keys=[user_id])

    def __init__(self, **kwargs):
        super(Comments, self).__init__(**kwargs)

    def __repr__(self):
        return '<Comment %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        return data


class Actions(Base):
    __tablename__ = "actions"

    details = db.Column(LONGTEXT, nullable=False)
    hash = db.Column(db.String(255), unique=True)

    def __init__(self, **kwargs):
        super(Actions, self).__init__(**kwargs)

    def __repr__(self):
        return '<Action %r>' % self.id

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        return data
