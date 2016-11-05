# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2

import main
# from main import JINJA_ENVIRONMENT as JINJA_ENVIRONMENT
# from google.appengine.api import users
# from datetime import datetime

__author__ = 'Daria'


class Competitions(webapp2.RequestHandler):

    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/test.html')
        self.response.write(template.render(temp_values))


class CertainCompetition(webapp2.RequestHandler):
    """
    Displays info about certain competition
    """
    def get(self):
        pass




