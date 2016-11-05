# -*- coding: utf-8 -*-
import os
import webapp2
#from google.appengine.api import users
#from datetime import datetime

__author__ = 'Daria'

'''
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
'''


class Test(webapp2.RequestHandler):
    def get(self):
        self.response.write('outside Test')


