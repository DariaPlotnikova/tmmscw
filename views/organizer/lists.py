import os
import jinja2
import webapp2

import main


class AllEntries(webapp2.RequestHandler):
    """
    Displays list of members/leaders/organizers and saves changes
    """
    def get(self):
        temp_values = {}
        if True:
            template = main.jinja_env.get_template('/tmmscw/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        elif 1 == 2:
            template = main.jinja_env.get_template('/tmmscw/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            template = main.jinja_env.get_template('/tmmscw/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))

    def post(self):
        temp_values = {}
        if True:
            template = main.jinja_env.get_template('/tmmscw/organizer/MemberList.html')
            self.response.write(template.render(temp_values))
        elif 1 == 2:
            template = main.jinja_env.get_template('/tmmscw/organizer/LeaderList.html')
            self.response.write(template.render(temp_values))
        else:
            template = main.jinja_env.get_template('/tmmscw/organizer/OrganizerList.html')
            self.response.write(template.render(temp_values))
