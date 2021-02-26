#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import event
from sqlalchemy.dialects.mysql import NVARCHAR, TINYINT

from flask_login import UserMixin
from flask_authorize import AllowancesMixin

from vhoops import app, db, Base
from vhoops.modules.teams.api.models import TeamMember

UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Users(Base, UserMixin):
    __tablename__ = "users"

    first_name = db.Column(NVARCHAR(64), nullable=False)
    last_name = db.Column(NVARCHAR(64), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(75), nullable=False)
    last_password_change = db.Column(db.DateTime)
    # Account statues: 1:Active, 2:Deleted, 3:Suspended
    account_status = db.Column(TINYINT, default=1)

    roles = db.relationship("Roles", secondary=UserRole)
    groups = db.relationship("Groups", secondary=UserGroup)
    teams = db.relationship("Teams", secondary=TeamMember)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return self.account_status

    def has_group(self, group_name):
        return group_name in [i.name for i in self.groups]

    @property
    def human_readable_groups(self):
        return ",".join([i.name for i in self.groups])

    @property
    def as_notification_dict(self):
        return dict(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            phone=self.phone_number
        )

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            if k.key not in ["password"]:
                data[k.key] = str(getattr(self, k.key))

        data["groups"] = ",".join([i.name for i in self.groups])
        data["teams"] = ",".join([i.name for i in self.teams])

        return data


class Groups(db.Model, AllowancesMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super(Groups, self).__init__(**kwargs)

    @property
    def as_dict(self):
        data = dict()
        for k in self.__table__.columns:
            data[k.key] = str(getattr(self, k.key))

        return data


class Roles(db.Model, AllowancesMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))


# Default data insert

def create_root_user(*args, **kwargs):
    db.session.add(
        Users(**app.config["ROOT_USER_DATA"])
    )
    db.session.commit()


def create_root_group(*args, **kwargs):
    root_group = Groups(**app.config["ROOT_GROUP_DATA"])

    root_user = Users.query.filter_by(username=app.config["ROOT_USER_DATA"]["username"]).first()
    root_user.groups = [root_group]

    db.session.add(root_group, root_user)
    db.session.commit()

    for group in app.config["INITIAL_GROUPS_DATA"]:
        db.session.add(Groups(**group))

    db.session.commit()


event.listen(Users.__table__, "after_create", create_root_user)
event.listen(UserGroup, "after_create", create_root_group)
