# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import datetime
from google.appengine.api import users


import main
from base_handlers import BaseHandler
from views.utils import info_from_db, diz_from_db, membs_from_db, format_date, find_user, create_roles_head,\
    format_date_list
from models.competition import MemInfo, DistInfo, Competition, Distance, Info, CompMemb


__author__ = 'Daria'


class Competitions(BaseHandler):
    """
    Displays list of competitions
    """
    def get(self):
        """Displays list of competition"""
        loc_role = self.session.get('role', 'anonim')
        comps = Competition.all().order('d_start')
        comps_count = comps.count()
        d_start = []
        d_finish = []
        pzs = []
        is_open_pz = []
        for c in comps:
            d_start.append(str(c.d_start))
            d_finish.append(str(c.d_finish))
            infos_of_comp = c.info_set.run(batch_size=1000)
            is_open = False
            for info_of_day in infos_of_comp:
                is_open = is_open or (info_of_day.pz_is_open and (datetime.datetime.today().date() < info_of_day.pz_add_end))
            is_open_pz.append(is_open)
        d_start = format_date_list(d_start)
        d_finish = format_date_list(d_finish)
        user = users.get_current_user()
        temp_values = {'comps': comps, 'c_count': comps_count, 'd_start': d_start,
                       'd_finish': d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz}
        if not user:        # user is anonim
            login = users.create_login_url(dest_url='/postSignIn')
            temp_values.update({'login': login, 'is_user': False})
            template = main.jinja_env.get_template('/tmmscw/CompetitionList.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = find_user(email)
            roles = create_roles_head(self, is_org, is_lead, is_memb)
            temp_values.update({'user_email': email, 'roles': roles, 'logout': users.create_logout_url('/'),
                                'is_user': True})

            if loc_role == 'organizer':          # show compList corresponding to user's role
                template_path = '/tmmscw/organizer/CompetitionList.html'
            elif loc_role == 'leader':
                template_path = '/tmmscw/leader/CompetitionList.html'
            elif loc_role == 'member':
                template_path = '/tmmscw/member/CompetitionList.html'
            else:         # user is anonim
                login = users.create_login_url(dest_url='/postSignIn')
                temp_values = {'login': login, 'comps': comps, 'c_count': comps_count, 'd_start': d_start, 'd_finish':
                            d_finish, 'pzs': pzs, 'is_open_pz': is_open_pz, 'logout': users.create_logout_url('/')}
                template_path = '/tmmscw/CompetitionList.html'
            template = main.jinja_env.get_template(template_path)
        self.response.write(template.render(temp_values))


class CertainCompetition(BaseHandler):
    """
    Displays info about certain competition
    """

    def get(self):
        """Displays info about competition stored in database"""
        user = users.get_current_user()
        key = self.request.get('comp_id')
        comp = Competition.get(key)
        info_values = info_from_db(comp)
        diz_values = diz_from_db(comp)
        memb_values = membs_from_db(comp)
        temp_values = {'start': format_date(str(comp.d_start)), 'finish': format_date(str(comp.d_finish)), 'name':
            comp.name, 'days_count': range(1, comp.days_count + 1), 'comp_id': comp.key()}
        temp_values.update(info_values)
        temp_values.update(diz_values)
        temp_values.update(memb_values)
        if not user:  # user is anonim
            login = users.create_login_url(dest_url='/postSignIn')
            temp_values.update({'action': webapp2.uri_for('add-by-day'), 'login': login})     # only one member
            template = main.jinja_env.get_template('/tmmscw/CertainCompetition.html')
        else:
            email = user.email()
            [is_org, is_lead, is_memb] = find_user(email)
            roles = create_roles_head(self, is_org, is_lead, is_memb)
            temp_values.update({'roles': roles, 'user_email': email, 'logout': users.create_logout_url('/')})
            if is_org and self.session.get('role') == 'organizer':
                action = ''
                template = main.jinja_env.get_template('/tmmscw/organizer/CertainCompetition.html')
            elif is_lead and self.session.get('role') == 'leader':
                action = webapp2.uri_for('add-by-day')
                template = main.jinja_env.get_template('/tmmscw/leader/CertainCompetition.html')
            elif is_memb and self.session.get('role') == 'member':
                action = webapp2.uri_for('add-by-day')  # only one member
                template = main.jinja_env.get_template('/tmmscw/member/CertainCompetition.html')
            else:
                action = webapp2.uri_for('add-by-day')  # only one member
                template = main.jinja_env.get_template('/tmmscw/CertainCompetition.html')
            temp_values.update({'action': action})
        self.response.write(template.render(temp_values))




