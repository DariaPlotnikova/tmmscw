# -*- coding: utf-8 -*-
from google.appengine.api import users

import main
from base_handlers import BaseHandler
from views.utils import create_roles, find_user


__author__ = 'Daria'


class PostSignIn(BaseHandler):

    def get(self):
        """Displays form for choosing current user role"""
        user = users.get_current_user()

        if not user:
            self.session['role'] = 'anonim'
            self.redirect('/')
        else:
            try:
                email = user.email()
                [is_org, is_lead, is_memb] = find_user(email)
                [roles, cur_role_local] = create_roles(is_org, is_lead, is_memb)
                if len(roles) > 1:      # If user has several roles, he should choose one
                    temp_values = {'roles': roles, 'logout': users.create_logout_url('/login')}
                    template = main.jinja_env.get_template('/tmmscw/AfterSignIn.html')
                    self.response.write(template.render(temp_values))
                else:                   # If user has only one role
                    self.session['role'] = cur_role_local
                    self.redirect('/')
            except Exception as e:                                     # If user hasn't roles in system (anonim)
                print 'Error at roles.PostSignIn: ' + str(e)
                self.session['role'] = 'anonim'
                self.redirect('/')

    def post(self):
        """Saves current user role"""
        cur_role_local = self.request.POST.get('curRole', 'anonim')
        self.session['role'] = cur_role_local
        self.redirect('/')


class BeforeSignOut(BaseHandler):

    def get(self):
        """Throws out current role before signing out of system"""
        self.session['role'] = 'anonim'
