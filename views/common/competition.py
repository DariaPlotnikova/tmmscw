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
        temp_values = {'user': user}

        template = main.jinja_env.get_template('/tmmscw/test.html')
        self.response.write(template.render(temp_values))


class CertainCompetition(webapp2.RequestHandler):
    """
    Displays info about certain competition
    """
    def get(self):
        pass




