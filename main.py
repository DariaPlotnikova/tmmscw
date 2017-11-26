#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import webapp2
import jinja2
from views import test
from views.common import roles
from views.common import competition as com_competition, members
from views.leader import competition as lead_competition, team
from views.organizer import competition as org_competition, lists
from views.member import views as memb_views


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
jinja_env.globals = {
    'url': webapp2.uri_for
}


config = dict()
config['webapp2_extras.sessions'] = {
    'secret_key': 'dadodorototo',
}
config['webapp2_extras.jinja2'] = {
    'template_path': 'templates',
    'globals': {
        'url': webapp2.uri_for,
    },
}


app = webapp2.WSGIApplication([
    # development routes
    webapp2.Route('/db', test.Db, name='test-db'),
    webapp2.Route('/test', test.Test, name='test'),
    webapp2.Route('/clean', test.CleanUp, name='clean'),
    # common routes
    webapp2.Route('/', com_competition.Competitions, name='comps'),
    webapp2.Route('/competition/', com_competition.CertainCompetition, name='comp'),
    webapp2.Route('/members', members.MemberList, name='members'),
    webapp2.Route('/postSignIn', roles.PostSignIn, name='post-singin'),
    webapp2.Route('/changeRole', roles.ChangeRole, name='change-role'),
    webapp2.Route('/reg/nullToRole', roles.BeforeSignOut, name='before-singout'),
    # member routes
    webapp2.Route('/member/edit', memb_views.EditMember, name='self-edit'),
    webapp2.Route('/member/check', memb_views.CheckPassToChange, name='check-pass'),
    webapp2.Route('/member/delete', memb_views.DeleteMember, name='self-delete'),
    webapp2.Route('/member/add_day', memb_views.AddMemberByDays, name='add-self-by-day'),
    webapp2.Route('/member/add_class', memb_views.AddMemberByClasses, name='add-self-by-class'),
    # leader routes
    webapp2.Route('/reg/lead/add_day', lead_competition.AddMembersByDays, name='add-by-day'),
    webapp2.Route('/reg/lead/add_class', lead_competition.AddMembersByClasses, name='add-by-class'),
    webapp2.Route('/reg/lead/team', team.Team, name='team'),
    webapp2.Route('/reg/lead/add_to_team', team.AddToTeam, name='add-to-team'),
    # webapp2.Route('/reg/lead/change', team.ChangeTeamMember, name='change-member'),
    webapp2.Route('/reg/lead/add_to_team/generate', team.GeneratePassToEdit, name='generate-pass-to-edit'),
    webapp2.Route('/reg/lead/delete', team.DeleteMember, name='delete-member'),
    # organizer routes
    #webapp2.Route('/reg/org/competition/(comp_id:\d+)', org_competition.CertainCompetition, name='comp-org'),
    webapp2.Route('/reg/org/fill_info', org_competition.FillCompetitionInfo, name='fillin-comp'),
    webapp2.Route('/reg/org/create', org_competition.CreateCompetition, name='create-comp'),

    webapp2.Route('/reg/org/list/organizer', lists.OrganizerList, name='list-orgs'),
    webapp2.Route('/reg/org/list/organizer/add', lists.OrganizerAdd, name='list-orgs-add'),
    webapp2.Route('/reg/org/list/organizer/delete', lists.OrganizerDelete, name='list-orgs-delete'),

    webapp2.Route('/reg/org/list/leader', lists.LeaderList, name='list-leads'),
    webapp2.Route('/reg/org/list/leader/add', lists.LeaderAdd, name='list-leads-add'),
    webapp2.Route('/reg/org/list/leader/delete', lists.LeaderDelete, name='list-leads-delete'),

    webapp2.Route('/reg/org/list/member', lists.MemberList, name='list-membs'),
    webapp2.Route('/reg/org/list/member/add', lists.MemberAdd, name='list-membs-add'),
    webapp2.Route('/reg/org/list/member/delete', lists.MemberDelete, name='list-membs-delete'),
], config=config, debug=True)


def handle_401(request, response, exception):
    response.set_status(401)
    temp_values = {'img_src': '../../../static/img/er401.png', 'er_name': '401', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def handle_403(request, response, exception):
    response.set_status(403)
    temp_values = {'img_src': '../../../static/img/er403.png', 'er_name': '403', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def handle_404(request, response, exception):
    response.set_status(404)
    temp_values = {'img_src': '../../../static/img/er404.png', 'er_name': '404', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def handle_405(request, response, exception):
    response.set_status(405)
    temp_values = {'img_src': '../../../static/img/er405.png', 'er_name': '405', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def handle_500(request, response, exception):
    response.set_status(500)
    temp_values = {'img_src': '../../../static/img/er500.png', 'er_name': '500', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def handle_503(request, response, exception):
    response.set_status(503)
    temp_values = {'img_src': '../../../static/img/er503.png', 'er_name': '503', 'request': request}
    response.write(jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


#app.error_handlers[401] = handle_401
#app.error_handlers[403] = handle_403
#app.error_handlers[404] = handle_404
#app.error_handlers[405] = handle_405
#app.error_handlers[500] = handle_500
#app.error_handlers[503] = handle_503
