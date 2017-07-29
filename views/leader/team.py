# -*- coding: utf-8 -*-
import webapp2
import time

import main

from google.appengine.api import users
from google.appengine.ext import db
from models.visitor import Member, Leader, Command
from ..decorators import current_leader_user
from ..utils import generate_passwd
# from main import JINJA_ENVIRONMENT as JINJA_ENVIRONMENT
# from google.appengine.api import users
# from datetime import datetime

__author__ = 'Daria'


class Team(webapp2.RequestHandler):
    """
    Displays and saves team of leader
    """
    @current_leader_user
    def get(self):
        user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', user).get()
        command = leader.command
        if not command:
            command = Command(name='', territory='')
        members = command.member_set
        temp_values = {'membs_count': members.count(), 'command': command, 'membs': members}
        template = main.jinja_env.get_template('/tmmscw/leader/Team.html')
        self.response.write(template.render(temp_values))

    @current_leader_user
    def post(self):
        user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', user).get()
        command = leader.command
        command.name = self.request.POST.get('nameTeam', command.name)
        command.territory = self.request.POST.get('terryTeam', command.territory)
        command.put()
        self.redirect(webapp2.uri_for('team'))


class AddToTeam(webapp2.RequestHandler):
    """
    Displays and saves new or changed member to team
    """
    @current_leader_user
    def get(self):
        edit_pass = generate_passwd()
        temp_values = {'new_memb': True, 'edit_pass': edit_pass}
        template = main.jinja_env.get_template('/tmmscw/leader/Member.html')
        self.response.write(template.render(temp_values))

    @current_leader_user
    def post(self):
        user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', user).get()
        command = leader.command
        edit_pass = self.request.POST.get('passToEdit')
        sex = self.request.POST.get('sexMemb')
        surname = self.request.POST.get('surnameMemb')
        birthdate = int(self.request.POST.get('birthdate'))
        qualification = self.request.POST.get('qualMemb')
        member = Member(pass_to_edit=edit_pass, sex=sex, surname=surname,
                        command=command, birthdate=birthdate, qualification=qualification)
        member.put()
        time.sleep(0.1)
        self.redirect(webapp2.uri_for('team'))


class ChangeTeamMember(webapp2.RequestHandler):
    @current_leader_user
    def get(self):
        member_key = self.request.GET.get('key')
        if member_key:
            member = Member.get(member_key)
            temp_values = {'member': member}
            template = main.jinja_env.get_template('/tmmscw/leader/ChangeMember.html')
            self.response.write(template.render(temp_values))
        else:
            webapp2.abort(404)

    @current_leader_user
    def post(self):
        member_key = self.request.POST.get('key')
        if member_key:
            member = Member.get(member_key)
            sex = self.request.POST.get('sexMemb')
            surname = self.request.POST.get('surnameMemb')
            birthdate = int(self.request.POST.get('birthdate'))
            qualification = self.request.POST.get('qualMemb')
            member.sex = sex
            member.surname = surname
            member.birthdate = birthdate
            member.qualification = qualification
            member.put()
            temp_values = {'member': member}
            template = main.jinja_env.get_template('/tmmscw/leader/ChangeMember.html')
            self.response.write(template.render(temp_values))
        else:
            webapp2.abort(404)


class DeleteMember(webapp2.RequestHandler):
    @current_leader_user
    def post(self):
        member_key = self.request.POST.get('key')
        if member_key:
            member = Member.get(member_key)
            user = users.get_current_user()
            leader = db.Query(Leader).filter('user =', user).get()
            print member.command.key()
            print leader.command.key()
            if member.command.key() == leader.command.key():
                member.delete()
                time.sleep(0.1)
                return self.redirect(webapp2.uri_for('team'))
        webapp2.abort(404)
