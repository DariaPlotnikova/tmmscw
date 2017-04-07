import os
import jinja2
import time
import webapp2
import main
from google.appengine.api import users
from google.appengine.ext import db
from models.visitor import Organizer
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
                               login_redir=users.create_login_url('reg/organizerList'))
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


class AllEntries(webapp2.RequestHandler):
    """
    Displays list of members/leaders/organizers and saves changes
    """
    def get(self):
        temp_values = {}
        if True:
            template = main.jinja_env.get_template('/tmmscw/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        elif 1 == 2:
            template = main.jinja_env.get_template('/tmmscw/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            template = main.jinja_env.get_template('/tmmscw/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))

    def post(self):
        temp_values = {}
        if True:
            template = main.jinja_env.get_template('/tmmscw/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        elif 1 == 2:
            template = main.jinja_env.get_template('/tmmscw/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            template = main.jinja_env.get_template('/tmmscw/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))
