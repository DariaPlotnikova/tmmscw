# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
from google.appengine.api import users

import main
from models import competition as comp_models, visitor

__author__ = 'Daria'


class Competitions(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        login = 'LOGIN'
        comps = []
        d_start = []
        d_finish = []
        pzs = []
        is_open_pz = []
        member = leader = organizer = False

        temp_values = {'login': login, 'comps': comps, 'c_count': 0, 'd_start': d_start, 'd_finish':
            d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz, 'logout': users.create_logout_url('/login')}

        if member:
            template = main.jinja_env.get_template('/tmmscw/member/CompetitionList.html')
        elif leader:
            template = main.jinja_env.get_template('/tmmscw/leader/CompetitionList.html')
        elif organizer:
            template = main.jinja_env.get_template('/tmmscw/organizer/CompetitionList.html')
        else:
            template = main.jinja_env.get_template('/tmmscw/CompetitionList.html')

        self.response.write(template.render(temp_values))


class CertainCompetition(webapp2.RequestHandler):
    """
    Displays info about certain competition
    """
    def get(self):
        member = leader = organizer = False

        temp_values = {}
        if member:
            template = main.jinja_env.get_template('/tmmscw/member/CertainCompetition.html')
        elif leader:
            template = main.jinja_env.get_template('/tmmscw/leader/CertainCompetition.html')
        elif organizer:
            template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
        else:
            template = main.jinja_env.get_template('/tmmscw/CertainCompetition.html')

        self.response.write(template.render(temp_values))




