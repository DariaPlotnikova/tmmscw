# -*- coding: utf-8 -*-
import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import db

import main
import defaults
from models.visitor import Member, Leader, Command
from ..decorators import current_leader_user
from ..utils import generate_passwd
from views.utils import create_roles_head, find_user
from ..common.base_handlers import BaseHandler

# from main import JINJA_ENVIRONMENT as JINJA_ENVIRONMENT
# from google.appengine.api import users
# from datetime import datetime

__author__ = 'Daria'


class Team(BaseHandler):
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
        email = user.email()
        loc_role = self.session.get('role', 'anonim')
        [is_org, is_lead, is_memb] = find_user(email)
        roles = create_roles_head(is_org, is_lead, is_memb)
        loc_role_rus = {'organizer': u'Организатор',
                        'leader': u'Руководитель команды',
                        'member': u'Участник',
                        'anonim': u'Аноним'}[loc_role]
        temp_values = {'membs_count': members.count(), 'command': command, 'membs': members,
                       'roles': roles, 'cur_role_rus': loc_role_rus, 'cur_role': loc_role,
                       'quals': defaults.DEFAULT_QUALS}
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


class AddToTeam(BaseHandler):
    """
    Displays and saves new or changed member to team
    """

    # @current_leader_user
    # def get(self):
    #     edit_pass = generate_passwd()
    #     temp_values = {'edit_pass': edit_pass}
    #     template = main.jinja_env.get_template('/tmmscw/leader/Member.html')
    #     self.response.write(template.render(temp_values))

    # @current_leader_user
    def post(self):
        user = users.get_current_user()
        if self.request.POST.get('lmKey'):  # change existing member
            new_surname = self.request.POST.get('lmFio')
            new_birthdate = int(self.request.POST.get('lmGr'))
            new_qual = self.request.POST.get('lmRazr')
            new_sex = self.request.POST.get('lmSexMemb')
            memb_key = self.request.POST.get('lmKey')

            member = Member.get(memb_key)
            member.sex = new_sex
            member.surname = new_surname
            member.birthdate = new_birthdate
            member.qualification = new_qual
            member.put()
        else:  # add new member
            leader = db.Query(Leader).filter('user =', user).get()
            command = leader.command
            edit_pass = self.request.POST.get('passToEdit')
            sex = self.request.POST.get('lmSexMemb')
            surname = self.request.POST.get('lmFio')
            birthdate = int(self.request.POST.get('lmGr'))
            qual = self.request.POST.get('lmRazr')
            new_member = Member(pass_to_edit=edit_pass, sex=sex, surname=surname,
                                command=command, birthdate=birthdate, qualification=qual)
            new_member.put()
        self.redirect(webapp2.uri_for('team'))

    # class ChangeTeamMember(webapp2.RequestHandler):
    # @current_leader_user
    # def get(self):
    #     member_key = self.request.GET.get('key')
    #     if member_key:
    #         member = Member.get(member_key)
    #         temp_values = {'member': member}
    #         template = main.jinja_env.get_template('/tmmscw/leader/ChangeMember.html')
    #         self.response.write(template.render(temp_values))
    #     else:
    #         webapp2.abort(404)
    #
    # @current_leader_user
    # def post(self):
    #     member_key = self.request.POST.get('key')
    #     if member_key:
    #         member = Member.get(member_key)
    #         sex = self.request.POST.get('sexMemb')
    #         surname = self.request.POST.get('surnameMemb')
    #         birthdate = int(self.request.POST.get('birthdate'))
    #         qualification = self.request.POST.get('qualMemb')
    #         member.sex = sex
    #         member.surname = surname
    #         member.birthdate = birthdate
    #         member.qualification = qualification
    #         member.put()
    #         temp_values = {'member': member}
    #         template = main.jinja_env.get_template('/tmmscw/leader/ChangeMember.html')
    #         self.response.write(template.render(temp_values))
    #     else:
    #         webapp2.abort(404)


class DeleteMember(webapp2.RequestHandler):
    @current_leader_user
    def post(self):
        member_key = self.request.POST.get('idMembKeyToDel')
        if member_key:
            member = Member.get(member_key)
            user = users.get_current_user()
            leader = db.Query(Leader).filter('user =', user).get()
            if member.command.key() == leader.command.key():
                member.delete()
                return self.redirect(webapp2.uri_for('team'))
        webapp2.abort(404)
