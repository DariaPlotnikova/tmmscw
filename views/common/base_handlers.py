import webapp2
import logging
from webapp2_extras import sessions

import main


__author__ = 'Daria'


class Test(webapp2.RequestHandler):

    def get(self):
        temp_values = {}
        template = main.jinja_env.get_template('/tmmscw/test.html')
        self.response.write(template.render(temp_values))


class BaseHandler(webapp2.RequestHandler):
    """
    This is the base class for views which enables
    working with sessions and logging server errors.
    """

    def handle_exception(self, exception, debug):
        logging.exception(exception)
        self.response.write('An error occurred.</br>')
        self.response.write(exception)

        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
