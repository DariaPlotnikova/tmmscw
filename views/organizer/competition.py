import os
import jinja2
import webapp2

import main


class CertainCompetition(webapp2.RequestHandler):
    """
    Displays full info about certain competition and listens ajax request with changes
    """
    def get(self):
        pass

    def post(self):     # ajax handler
        pass            # TODO create handler as kanban in Brama (if field='')


class FillCompetitionInfo(webapp2.RequestHandler):
    """
    Saves common info about new competition
    """
    def get(self):
        pass

    def post(self):
        pass


class CreateCompetition(webapp2.RequestHandler):
    """
    Saves full info about new competition
    """
    def get(self):
        pass

    def post(self):
        pass
