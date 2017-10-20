# -*- coding: utf-8 -*-
import webapp2
import main

from google.appengine.api import users
from google.appengine.ext import db

from models.visitor import Member
from models.competition import Competition, CompMemb
import defaults
from ..utils import create_roles_head, find_user
from ..common.base_handlers import BaseHandler


class EditMember(BaseHandler):
    """ Displays detailed info about member and edit it using his confirmation code """

    def get(self):
        user = users.get_current_user()
        member = db.Query(Member).filter('user =', user).get()
        if member:
            email = user.email()
            loc_role = self.session.get('role', 'anonim')
            [is_org, is_lead, is_memb] = find_user(email)
            roles = create_roles_head(is_org, is_lead, is_memb)
            loc_role_rus = {'organizer': u'Организатор',
                            'leader': u'Руководитель команды',
                            'member': u'Участник',
                            'anonim': u'Аноним'}[loc_role]
            temp_values = {'user_email': email, 'member': member, 'quals': defaults.DEFAULT_QUALS,
                           'roles': roles, 'cur_role_rus': loc_role_rus, 'cur_role': loc_role}
            template = main.jinja_env.get_template('/tmmscw/member/MemberEdit.html')
            self.response.write(template.render(temp_values))
        else:
            webapp2.abort(404)

    def post(self):
        user = users.get_current_user()
        member = db.Query(Member).filter('user =', user).get()
        if member:
            new_surname = self.request.POST.get('surnameMemb')
            new_birthday = int(self.request.POST.get('birthdayMemb'))
            new_qual = self.request.POST.get('qualMemb')
            member.surname = new_surname
            member.birthdate = new_birthday
            member.qualification = new_qual
            member.put()
            self.redirect(webapp2.uri_for('self-edit'))
        else:
            webapp2.abort(404)


class DeleteMember(webapp2.RequestHandler):
    """ Delete one member using his confirmation code """
    pass


class CheckPassToChange(BaseHandler):
    def get(self):
        pass

    def post(self):
        user = users.get_current_user()
        member = db.Query(Member).filter('user =', user).get()
        if member:
            temp_pass = self.request.POST.get('pass')
            print(str(member.pass_to_edit), str(temp_pass))
            if str(member.pass_to_edit) == str(temp_pass):
                self.response.out.write('true')
            else:
                self.response.out.write('false')

        else:
            webapp2.abort(404)


'''
@current_leader_user
def get(self):
    comp_key = self.request.GET.get('competition')
    if comp_key:
        competition = Competition.get(comp_key)
        user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', user).get()
        command = leader.command
        comp_members = competition.compmemb_set
        team_members = command.member_set
        entry_membs = [m for m in team_members if m in comp_members]
        no_entry_membs = [m for m in team_members if m not in comp_members]
        temp_values = {'competition': competition, 'entry_membs': entry_membs,
                       'no_entry_membs': no_entry_membs, 'days_range': range(competition.days_count)}
        template = main.jinja_env.get_template('/tmmscw/leader/MembersToCompetition.html')
        self.response.write(template.render(temp_values))
    else:
        webapp2.abort(404)

@current_leader_user
def post(self):
    comp_key = self.request.get('competition')
    if comp_key:
        competition = Competition.get(comp_key)
        membs_by_day = []
        dists = []
        groups = []
        for d in range(competition.days_count):
            membs = [Member.get(key) for key in self.request.get_all('checkMemb%d' % d)]
            membs_by_day.append(membs)
            day_distance = competition.distance_set.filter('day_numb =', d).get()
            dists.append(day_distance)
            groups.append(day_distance.distinfo_set)
        temp_values = {'membs_by_day': membs_by_day, 'dists': dists, 'groups': groups, 'competition': competition}
        template = main.jinja_env.get_template('/tmmscw/leader/MembersToDays.html')
        self.response.write(template.render(temp_values))
'''


class AddMemberByDays(webapp2.RequestHandler):
    """ Add member to competition for days """

    def get(self):
        comp_key = self.request.GET.get('competition')
        if comp_key:
            competition = Competition.get(comp_key)
            members = Member.all()
            comp_members = [cm.member for cm in competition.compmemb_set]
            entry_membs = [m for m in members if m in comp_members]
            no_entry_membs = [m for m in members if m not in comp_members]
            temp_values = {'competition': competition, 'entry_membs': entry_membs,
                           'no_entry_membs': no_entry_membs, 'days_range': range(competition.days_count),
                           'comp_members': comp_members}
            template = main.jinja_env.get_template('/tmmscw/member/MemberToCompetition.html')
            self.response.write(template.render(temp_values))
        else:
            webapp2.abort(404)

    def post(self):
        pass


'''
@current_leader_user
def post(self):
    comp_key = self.request.get('competition')
    if comp_key:
        competition = Competition.get(comp_key)
        for d in range(competition.days_count):
            dist_key = self.request.get('group_day%d' % d)
            for post_key in self.request.POST.keys():
                memb_post_key = re.match(r'memb_for_day%d\d+' % d, post_key)
                if memb_post_key:
                    members_keys = self.request.get_all(memb_post_key.string)
                    distance = DistInfo.get(dist_key)
                    for key in members_keys:
                        member = Member.get(key)
                        memb_for_day = CompMemb(competition=competition, member=member, group=distance, day_numb=d)
                        memb_for_day.put()
        return self.redirect(webapp2.uri_for('comp', comp_id=comp_key))
    else:
        webapp2.abort(404)
'''


class AddMemberByClasses(webapp2.RedirectHandler):
    """ Add member to competition's classes for each selected day """
    pass
