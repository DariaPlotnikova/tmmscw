import os
import jinja2
import webapp2
from google.appengine.api import users

import main
from views.utils import show_unauth_page, find_user, create_roles_head, format_date,\
    post_competition, post_info, post_diz
from views.common.base_handlers import BaseHandler

'''
class CertainCompetition(webapp2.RedirectHandler, BaseHandler):
    """
    Displays full info about certain competition and listens ajax request with changes
    """
    def get(self, comp_id):
        competition = 1
        temp_values = {'competition': competition}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))

    def post(self):     # ajax handler
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))
'''

class FillCompetitionInfo(webapp2.RedirectHandler, BaseHandler):
    """
    Saves common info about new competition
    """
    def get(self):
        """Displays empty form for adding common info of that new competition"""
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

    def post(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            name = self.request.POST.get('nameCompNew')
            d_s = self.request.POST.get('dateStartNew')
            d_f = self.request.POST.get('dateFinishNew')
            d_count = self.request.POST.get('countStart')
            write_places = self.request.POST.get('checkPlaces', False)
            show_map = self.request.POST.get('checkPlacesMap', False)

            temp_values = dict(user_email=email, logout=users.create_logout_url('/login'), d_start=format_date(d_s),
                               d_finish=format_date(d_f), name=name, days_count=range(1, int(d_count) + 1),
                               write_places=write_places, show_map=show_map, d_count=d_count)
            template = main.jinja_env.get_template('/tmmscw/organizer/AddCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            show_unauth_page(self)


class CreateCompetition(webapp2.RedirectHandler, BaseHandler):
    """
    Saves full info about new competition
    """
    def post(self):
        user = users.get_current_user()
        if user:
            competition, temp_values, errors = post_competition(self)
            temp_values.update(post_info(self, competition))
            temp_values.update(post_diz(self, competition))
            template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            show_unauth_page(self)

        '''
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        self.response.write(template.render(temp_values))
        '''
