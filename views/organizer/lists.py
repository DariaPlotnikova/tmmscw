import os
import jinja2
import webapp2

import main


class AllEntries(webapp2.RequestHandler):
    """
    Displays list of members/leaders/organizers and saves changes
    """
    def get(self):
        pass

    def post(self):
        pass            # TODO create handler as kanban in Brama (if kind='')
