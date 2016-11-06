import os
import jinja2
import webapp2

import main


class CertainCompetition(webapp2.RequestHandler):
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


class FillCompetitionInfo(webapp2.RequestHandler):
    """
    Saves common info about new competition
    """
    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/organizer/NewCompetitionInfo.html')
        self.response.write(template.render(temp_values))

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
