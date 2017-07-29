# -*- coding: utf-8 -*-
from google.appengine.ext import db
import defaults

__author__ = 'Daria'


class Organizer(db.Model):
    user = db.UserProperty(auto_current_user_add=False)
    nickname = db.StringProperty(required=False, multiline=False)
    contact = db.StringProperty(required=False)

    @classmethod
    def get_by_user(cls, user):
        return db.Query(cls).filter(cls.user_id == user.user_id()).get()


class Command(db.Model):
    name = db.StringProperty()
    territory = db.StringProperty(multiline=False)


class Leader(db.Model):
    user = db.UserProperty(auto_current_user_add=False)
    command = db.ReferenceProperty(Command)
    nickname = db.StringProperty(multiline=False)
    contact = db.EmailProperty(required=True)

    @classmethod
    def get_by_user(cls, user):
        return db.Query(cls).filter(cls.user_id == user.user_id()).get()


class Member(db.Model):
    pass_to_edit = db.StringProperty(multiline=False)
    sex = db.StringProperty(multiline=False)
    nickname = db.StringProperty(multiline=False)
    surname = db.StringProperty(required=False, multiline=False)
    command = db.ReferenceProperty(Command, required=False)
    birthdate = db.IntegerProperty(required=True)
    qualification = db.StringProperty(choices=defaults.DEFAULT_QUALS, default=defaults.DEFAULT_QUALS[0])

    @classmethod
    def get_by_user(cls, user):
        return db.Query(cls)\
            .filter(cls.user_id == user.user_id()).get()
