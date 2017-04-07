import os
import jinja2
import time
import webapp2
import main, defaults
from google.appengine.api import users
from google.appengine.ext import db
from models.visitor import Organizer, Leader, Member, Command

from ..common.base_handlers import BaseHandler

# TODO change globals to something else
tooltip_message = ''
tooltip_show = 'none'


class OrganizerList(BaseHandler):
    """
    Displays list of organizers
    """
    def get(self):
        user = users.get_current_user()
        if user:
            orgs = db.Query(Organizer).order('nickname')
            keys = []
            for org in orgs:
                keys.append(org.key())
            global tooltip_message
            global tooltip_show
            temp_values = dict(user_email=user.email(), logout=users.create_logout_url('/login'),
                               disp_tool=tooltip_show, tool=tooltip_message, organizers=orgs, keys=keys)
            template = main.jinja_env.get_template('/tmmscw/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = dict(img_src='/static/img/er401.png', er_name='401',
                               login_redir=users.create_login_url(webapp2.uri_for('list-orgs')))
            self.response.write(main.jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


class OrganizerAdd(BaseHandler):
    """
    Add new organizer and change existed
    """
    def post(self):
        if self.request.POST.get('olKey'):      # changing existing organizer
            new_fio = self.request.POST.get('olFio')
            new_contact = self.request.POST.get('olContact')
            org_key = self.request.POST.get('olKey')
            organizer = Organizer.get(org_key)
            organizer.nickname = new_fio
            organizer.contact = new_contact
            organizer.put()
            tooltip_message = u'Organizer %s changed' % new_fio
        else:                               # add new organizer
            fio = self.request.POST.get('olFio')
            contact = self.request.POST.get('olContact')
            newOrg = Organizer(nickname=fio, contact=contact)
            newOrg.put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Organizer %s added to database' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect(webapp2.uri_for('list-orgs'))


class OrganizerDelete(BaseHandler):
    def post(self):
        org_id = self.request.POST.get('idToDeleteChange')
        fio = self.request.POST.get('organFio')
        db.delete(org_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Organizer %s deleted' % fio
        tooltip_show = 'block'
        self.redirect(webapp2.uri_for('list-orgs'))


class LeaderList(BaseHandler):
    """
    Displays list of leaders
    """
    def get(self):
        user = users.get_current_user()
        if user:
            leaders = db.Query(Leader).order('nickname')
            keys = []
            for lead in leaders:
                keys.append(lead.key())
            global tooltip_message
            global tooltip_show
            temp_values = dict(user_email=user.email(), logout=users.create_logout_url('/login'),
                               disp_tool=tooltip_show, tool=tooltip_message, leads=leaders, keys=keys)
            template = main.jinja_env.get_template('/tmmscw/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = dict(img_src='/static/img/er401.png', er_name='401',
                               login_redir=users.create_login_url(webapp2.uri_for('list-leads')))
            self.response.write(main.jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


class LeaderAdd(BaseHandler):
    """
    Add new leader and change existed
    """
    def post(self):
        if self.request.POST.get('llKey'):              # changing existing leader
            new_fio = self.request.POST.get('llFio')
            new_contact = self.request.POST.get('llContact')
            lead_key = self.request.POST.get('llKey')
            leader = Leader.get(lead_key)
            leader.nickname = new_fio
            leader.contact = new_contact
            leader.put()
            new_command = self.request.POST.get('llComand')
            new_terry = self.request.POST.get('llTerritory')
            leader.command.name = new_command
            leader.command.territory = new_terry
            leader.command.put()
            tooltip_message = u'Leader %s changed' % new_fio
        else:                                           # add new leader
            command = self.request.POST.get('llComand')
            terry = self.request.POST.get('llTerritory')
            command = Command(name=command, territory=terry).put()
            fio = self.request.POST.get('llFio')
            contact = self.request.POST.get('llContact')
            Leader(nickname=fio, contact=contact, command=command).put()
            global tooltip_message
            global tooltip_show
            tooltip_message = u'Leader %s was added to database' % fio
        tooltip_show = 'block'
        time.sleep(0.1)
        self.redirect(webapp2.uri_for('list-leads'))


class LeaderDelete(BaseHandler):
    def post(self):
        lead_id = self.request.POST['idToDeleteChange']
        fio = self.request.POST['leadFio']
        db.delete(lead_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Leader %s was deleted' % fio
        tooltip_show = 'block'
        self.redirect(webapp2.uri_for('list-leads'))


class MemberList(BaseHandler):
    """
    Displays list of members
    """
    def get(self):
        user = users.get_current_user()
        if user:
            members = db.Query(Member).order('nickname')
            keys = []
            for memb in members:
                keys.append(memb.key())
            global tooltip_message
            global tooltip_show
            commands = db.Query(Command)
            temp_values = dict(user_email=user.email(), logout=users.create_logout_url('/login'),
                               disp_tool=tooltip_show, tool=tooltip_message, members=members, keys=keys,
                               commands=commands, quals=defaults.DEFAULT_QUALS)
            template = main.jinja_env.get_template('/tmmscw/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        else:
            temp_values = dict(img_src='/static/img/er401.png', er_name='401',
                               login_redir=users.create_login_url(webapp2.uri_for('list-membs')))
            self.response.write(main.jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


class MemberAdd(BaseHandler):
    """
    Add new member and change existed
    """
    def post(self):
        cur_user = users.get_current_user()
        if cur_user:
            if self.request.POST.get('omKey'):              # change existing member
                new_fio = self.request.POST.get('omFio')
                new_birthdate = self.request.POST.get('omGr')
                new_qual = self.request.POST.get('omRazr')
                new_command_id = self.request.POST.get('omComand')
                new_command = db.Query(Command).filter('__key__ =', db.Key(new_command_id)).get()
                memb_key = self.request.POST.get('omKey')
                member = Member.get(memb_key)
                member.nickname = new_fio
                member.command = new_command
                member.birthdate = int(new_birthdate)
                member.qualification = new_qual
                member.put()
                tooltip_message = u'Member %s was changed' % new_fio
            else:                                           # add new member
                comm_id = self.request.POST.get('omComand')
                command = db.Query(Command).filter('__key__ =', db.Key(comm_id)).get()
                fio = self.request.POST.get('omFio')
                bdate = int(self.request.POST.get('omGr'))
                qual = self.request.POST.get('omRazr')
                new_member = Member(nickname=fio, birthdate=bdate, qualification=qual, command=command)
                new_member.put()
                global tooltip_message
                global tooltip_show
                tooltip_message = u'Member %s was added to database' % fio
            tooltip_show = 'block'
            time.sleep(0.1)
            self.redirect(webapp2.uri_for('list-membs'))
        else:
            temp_values = dict(img_src='/static/img/er401.png', er_name='401',
                               login_redir=users.create_login_url(webapp2.uri_for('list-membs')))
            self.response.write(main.jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


class MemberDelete(BaseHandler):
    def post(self):
        memb_id = self.request.POST.get('idToDeleteChange')
        fio = self.request.POST.get('membFio')
        db.delete(memb_id)
        time.sleep(0.1)
        global tooltip_message
        global tooltip_show
        tooltip_message = u'Member %s was deleted' % fio
        tooltip_show = 'block'
        self.redirect(webapp2.uri_for('list-membs'))
