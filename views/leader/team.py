# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2

import main
# from main import JINJA_ENVIRONMENT as JINJA_ENVIRONMENT
# from google.appengine.api import users
# from datetime import datetime

__author__ = 'Daria'


class Team(webapp2.RequestHandler):
    """
    Displays and saves team of leader
    """
    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/Team.html')
        self.response.write(template.render(temp_values))

    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/Team.html')
        self.response.write(template.render(temp_values))


class AddToTeam(webapp2.RequestHandler):
    """
    Displays and saves new or changed member to team
    """
    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/Member.html')
        self.response.write(template.render(temp_values))

    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/Team.html')
        self.response.write(template.render(temp_values))





