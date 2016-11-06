# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2

import main
# from main import JINJA_ENVIRONMENT as JINJA_ENVIRONMENT
# from google.appengine.api import users
# from datetime import datetime

__author__ = 'Daria'


class AddMembersByDays(webapp2.RequestHandler):
    """
    Add team members to days of competition
    """
    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/MembersToCompetition.html')
        self.response.write(template.render(temp_values))

    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/MembersToDays.html')
        self.response.write(template.render(temp_values))


class AddMembersByClasses(webapp2.RequestHandler):
    """
    Add team members to class for each day in competition
    """
    def post(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/leader/CertainCompetition.html')
        self.response.write(template.render(temp_values))





