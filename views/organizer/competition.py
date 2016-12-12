import os
import jinja2
import webapp2
from google.appengine.api import users

import main
from views.utils import show_unauth_page, find_user, create_roles_head
from views.common.base_handlers import BaseHandler


class CertainCompetition(BaseHandler):
    """
    Displays full info about certain competition and listens ajax request with changes
    """
    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))

    def post(self):     # ajax handler  # TODO create handler as kanban in Brama (if field='')
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))


class FillCompetitionInfo(BaseHandler):
    """
    Saves common info about new competition
    """
    def get(self):
        """Displays empty form for adding common info of that new competition"""
        try:
            user = users.get_current_user()
            if not user:
                show_unauth_page(self)
            else:
                email = user.email()
                [is_org, is_lead, is_memb] = find_user(email)
                roles = create_roles_head(self, is_org, is_lead, is_memb)
                if is_org and self.session.get('role') == 'organizer':
                    temp_values = {'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/')}
                    template = main.jinja_env.get_template('/tmmscw/organizer/NewCompetitionInfo.html')
                    self.response.write(template.render(temp_values))
                else:
                    show_unauth_page(self)
        except Exception as e:
            print '____________________________\nError:' + str(e.message)
        '''
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/NewCompetitionInfo.html')
        self.response.write(template.render(temp_values))
        '''

    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/AddCompetition.html')
        self.response.write(template.render(temp_values))


class CreateCompetition(webapp2.RequestHandler):
    """
    Saves full info about new competition
    """
    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))
