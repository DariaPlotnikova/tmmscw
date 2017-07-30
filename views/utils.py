# -*- coding: utf-8 -*-
import hashlib
import random
import string
from google.appengine.api import users
from datetime import date, datetime
from google.appengine.ext import db

import main
from models.competition import MemInfo, DistInfo, Competition, Distance, Info, CompMemb
from models.visitor import Organizer, Leader, Member


__author__ = 'Daria'


def generate_passwd():
    pwd = []
    for i in range(3):
        pwd.append(random.choice(string.ascii_lowercase))
        pwd.append(random.choice(string.ascii_uppercase))
    random.shuffle(pwd)
    return ''.join(pwd)


def salt_pass(paswd):
    """Salts user's password"""
    md = hashlib.md5()
    md.update(paswd)
    md.update('dado')       # This is salt
    return md.hexdigest()


def show_unauth_page(self):
    """
    Check is user authorized to look at some secured part of the system
    """
    temp_values = {'img_src': '/static/img/er401.png', 'er_name': '401', 'login_redir':
                    users.create_login_url('/postSignIn')}
    self.response.write(main.jinja_env.get_template('/tmmscw/errors.html').render(temp_values))


def format_date(bad_date):
    """Converts date from 'dd-mm-yyyy' to 'dd.mm.yyyy'"""
    ymd = bad_date.split('-')
    y = ymd[0]
    m = ymd[1]
    d = ymd[2]
    return '%s.%s.%s' % (str(d), str(m), str(y))


def format_date_list(bad_date_list):
    """Converts list of dates. Each date from 'dd-mm-yyyy' to 'dd.mm.yyyy'"""
    return [format_date(d) for d in bad_date_list]


def date_to_python(string_date):
    """Converts string representation of date to python date type"""
    if '.' in string_date:
        dmy = string_date.split('.')
        d = int(dmy[0])
        m = int(dmy[1])
        y = int(dmy[2])
        return date(y, m, d)
    else:
        ymd = string_date.split('-')
        y = ymd[0]
        m = ymd[1]
        d = ymd[2]
        return date(y, m, d)


def on_to_checked(check_list):
    """Converts list of checkbox's values to list of 'checked' or '' values"""
    return ['checked' if str(check).find('on') > 0 else '' for check in check_list]


def on_to_boolean(on_off):
    """Converts checkbox's value to boolean value"""
    if str(on_off).find('on') > 0:
        return True
    else:
        return False


def bool_to_checked(bool_value):
    """Converts boolean to string value 'checked' or ''"""
    if bool_value:
        return 'checked'
    else:
        return ''


def read_checkbox_post(request, post_name):
    """Reads checkbox's value from post-request and returns corresponding boolean"""
    try:
        bool_value = request.request.POST[post_name]
        bool_value = True
    except:
        bool_value = False
    return bool_value


def read_checkbox_get(request, get_name):
    """Reads checkbox's value from get-request and returns corresponding boolean"""
    try:
        bool_value = request.request.GET[get_name]
        bool_value = True
    except:
        bool_value = False
    return bool_value


def get_common_info(self):
    """Reads common info about competition from get-request and fills template's values"""
    name = self.request.GET['nameCompNew']
    d_s = self.request.GET['dateStartNew']
    d_f = self.request.GET['dateFinishNew']
    d_count = self.request.GET['countStart']
    write_places = read_checkbox_get(self, 'checkPlaces')
    show_map = read_checkbox_get(self, 'checkPlacesMap')
    temp_values = {'logout': users.create_logout_url('/login'), 'd_start': format_date(d_s), 'd_finish': format_date(d_f),
                   'name': name, 'days_count': range(1, int(d_count) + 1), 'write_places': write_places, 'show_map':
                   show_map, 'd_count': d_count}
    return temp_values


def post_competition(self):
    """Reads common info about competition and statistic flags from post-request and fills template's values"""
    try:
        errors = []
        start_date = self.request.POST['dateStartNew']
        #if start_date >= datetime.now():           # TODO: error because start_date is string not datetime object. Convert string to date
        #    pass
        finish_date = self.request.POST['dateFinishNew']
        #if finish_date >= datetime.now():
        #    pass#errors.append('Finish date in the past')
        comp_name = self.request.POST['nameCompNew']
        d_count = int(self.request.POST['dayCount'])
        show_places = self.request.POST['writePlaces']
        show_map = self.request.POST['showMap']
        stat_day = read_checkbox_post(self, 'statistic0')       #TODO: fix statistic
        stat_sex = read_checkbox_post(self, 'statistic1')
        stat_qual = read_checkbox_post(self, 'statistic2')
    except KeyError:
        errors.append('Key error at request')
    competition = Competition(name=comp_name, d_start=date_to_python(start_date), d_finish=date_to_python(finish_date),
                              days_count=d_count)#, statistic=[stat_day, stat_sex, stat_qual])
    competition.put()
    temp_values = {'start': start_date, 'finish': finish_date, 'name': comp_name, 'show_places': show_places,
                   'show_map': show_map, 'days_count': range(1, int(d_count) + 1)}
    return [competition, temp_values, errors]


def post_info(self, competition):
    """Reads common info about competition from post-request and fills template's values"""
    pz_end_add = format_date_list(self.request.POST.getall('pzEndAddNew'))
    pz_end_change = format_date_list(self.request.POST.getall('pzEndChangeNew'))
    links = self.request.POST.getall('toTmMoscowNew')
    places = self.request.POST.getall('placeNew')
    pzs = []
    tzs = []
    org_fios = []
    org_dols = []
    org_conts = []
    org_infos = []
    for i in range(1, competition.days_count + 1):
        pzs.append(self.request.POST.getall('trPzNew%s' % str(i)))
        tzs.append(self.request.POST.getall('trTzNew%s' % str(i)))
        org_fios.append(self.request.POST.getall('orgFioNew%s' % str(i)))
        org_dols.append(self.request.POST.getall('orgDolNew%s' % str(i)))
        org_conts.append(self.request.POST.getall('orgContNew%s' % str(i)))
    for i in range(competition.days_count):
        info = Info(competition=competition, day_numb=i, place_addr=places[i], pz_is_open=on_to_boolean(pzs[i]),
                    pz_add_end=date_to_python(pz_end_add[i]), pz_change_end=date_to_python(pz_end_change[i]),
                    tz_is_on=on_to_boolean(tzs[i]), link=links[i], orgs_fio=org_fios[i], orgs_dol=org_dols[i],
                    orgs_cont=org_conts[i])
        info.put()
    pzs = on_to_checked(pzs)
    tzs = on_to_checked(tzs)
    temp_values = {'pz_end_add': pz_end_add, 'pz_end_change': pz_end_change, 'links': links, 'places': places,
                   'pzs': pzs, 'tzs': tzs, 'org_fios': org_fios, 'org_dols': org_dols, 'org_conts': org_conts,
                   'org_infos': org_infos}
    return temp_values


def post_diz(self, competition):
    """Reads distance's info of competition from post-request and fills template's values"""
    disciplines = []
    lengths = []
    dizs = []
    dus = []
    diz_groups = []
    diz_length = []
    diz_class = []
    diz_min_com = []
    diz_max_com = []
    du_group = []
    du_salary = []
    du_age_min = []
    du_age_max = []
    du_qual_min = []
    du_qual_max = []
    for i in range(1, competition.days_count + 1):
        disciplines.append(self.request.POST['dizDisciplineNew%s' % str(i)])
        lengths.append(self.request.POST['dizLengthNew%s' % str(i)])
        diz_groups.append(self.request.POST.getall('dizGroupNew%s' % str(i)))
        diz_length.append(self.request.POST.getall('dizLenNew%s' % str(i)))
        diz_class.append(self.request.POST.getall('dizClassNew%s' % str(i)))
        diz_min_com.append(self.request.POST.getall('dizCCminNew%s' % str(i)))
        diz_max_com.append(self.request.POST.getall('dizCCmaxNew%s' % str(i)))
        du_group.append(self.request.POST.getall('duGroupNew%s' % str(i)))
        du_salary.append(self.request.POST.getall('duSalaryNew%s' % str(i)))
        du_age_min.append(self.request.POST.getall('duAgeminNew%s' % str(i)))
        du_age_max.append(self.request.POST.getall('duAgemaxNew%s' % str(i)))
        du_qual_min.append(self.request.POST.getall('duQualNewmin%s' % str(i)))
        du_qual_max.append(self.request.POST.getall('duQualNewmax%s' % str(i)))
    for i in range(competition.days_count):  # Run through days
        distance = Distance(competition=competition, day_numb=i, type=disciplines[i], lent=lengths[i])
        distance.put()
        dizs.append(zip(diz_groups[i], diz_length[i], diz_class[i], diz_min_com[i], diz_max_com[i]))
        dus.append(zip(du_group[i], du_salary[i], du_age_min[i], du_age_max[i], du_qual_min[i], du_qual_max[i]))
        for j in range(len(du_group[i])):  # Run through groups in one day
            mem = MemInfo(salary=float(du_salary[i][j]), age_min=int(du_age_min[i][j]), ordering=j,
                          age_max=int(du_age_max[i][j]), qual_min=du_qual_min[i][j], qual_max=du_qual_max[i][j])
            mem.put()
            dist = DistInfo(group_name=diz_groups[i][j], length=float(diz_length[i][j]),
                            dist_class=int(diz_class[i][j]), min_com=int(diz_min_com[i][j]),
                            max_com=int(diz_max_com[i][j]), mem_info=mem, distance=distance, ordering=j)
            dist.put()
    temp_values = {'discs': disciplines, 'lens': lengths, 'dizs': dizs, 'dus': dus, 'stat_day': competition.statistic[0],
                   'stat_sex': competition.statistic[1], 'stat_qual': competition.statistic[2], 'membs_count': 0}
    return temp_values


def info_from_db(comp):
    """Gets common info about competition from database and fills template's values"""
    infos = comp.info_set.run(batch_size=1000)
    pz_end_add = []
    pz_end_change = []
    pzs = []
    tzs = []
    places = []
    links = []
    orgs_fio = []
    orgs_dol = []
    orgs_cont = []
    org_infos = []
    for info in infos:
        day_numb_of_info = info.day_numb
        pz_end_add.insert(day_numb_of_info, format_date(str(info.pz_add_end)))
        pz_end_change.insert(day_numb_of_info, format_date(str(info.pz_change_end)))
        pzs.insert(day_numb_of_info, bool_to_checked(info.pz_is_open and (datetime.today().date() < info.pz_add_end)))
        tzs.insert(day_numb_of_info, bool_to_checked(info.tz_is_on))
        places.insert(day_numb_of_info, info.place_addr)
        links.insert(day_numb_of_info, info.link)
        day_info = []
        for idx, fio in enumerate(info.orgs_fio):
            day_info.append(dict(fio=fio, dol=info.orgs_dol[idx], cont=info.orgs_cont[idx]))
        org_infos.insert(day_numb_of_info, day_info)
    temp_values = {'pz_end_add': pz_end_add, 'pz_end_change': pz_end_change, 'places': places, 'pzs': pzs, 'tzs': tzs,
                   'links': links, 'org_fios': orgs_fio, 'org_dols': orgs_dol, 'org_conts': orgs_cont,
                   'org_infos': org_infos}
    return temp_values


def diz_from_db(comp):
    """Gets distance's info of competition from database and fills template's values"""
    distances_of_comp = comp.distance_set.run(batch_size=1000)
    disciplines = []
    lengths = []
    dizs = []
    dus = []
    for distance in distances_of_comp:
        day_numb_of_distance = distance.day_numb
        disciplines.insert(day_numb_of_distance, distance.type)
        lengths.insert(day_numb_of_distance, distance.lent)
        dists_info = distance.distinfo_set.run(batch_size=1000)
        dizs_of_day = []
        dus_of_day = []
        for dist in dists_info:
            dizs_of_day.append(dist)
            mem_info = dist.mem_info
            dus_of_day.append(dict(salary=mem_info.salary, age_min=mem_info.age_min,
                                   age_max=mem_info.age_max, qual_min=mem_info.qual_min,
                                   qual_max=mem_info.qual_max, group=dist.group_name))
            print dizs_of_day
        dizs.insert(day_numb_of_distance, dizs_of_day)
        dus.insert(day_numb_of_distance, dus_of_day)
    temp_values = {'discs': disciplines, 'lens': lengths, 'dizs': dizs, 'dus': dus}
    return temp_values


def membs_from_db(comp):
    """Gets members of the competition from database and fills template's values"""
    members_by_day = []
    membs_count = 0
    for day in range(1, comp.days_count + 1):
        membs_of_day_q = db.Query(CompMemb).filter('competition =', comp).filter('day_numb =', day).order('group')
        membs_of_day = membs_of_day_q.run(batch_size=1000)
        if membs_of_day_q.count() > 0:
            membs_count = 1
        members_by_day.append(membs_of_day)
    temp_values = {'membs_by_days': members_by_day, 'membs_count': membs_count}
    return temp_values


def find_user(keyword):
    """Checks is user in database"""
    is_org = db.Query(Organizer).filter('contact =', keyword).count()
    is_lead = db.Query(Leader).filter('contact =', keyword).count()
    is_memb = db.Query(Member).filter('nickname =', keyword).count()
    return [is_org, is_lead, is_memb]


def create_roles_head(self, is_org, is_lead, is_memb):
    """Returns list of registered user roles for indicating available roles at page head"""
    roles = []
    if is_org:
        if self.session.get('role') == 'organizer':
            roles.append(u'<b>ORG</b>')
        else:
            roles.append(u'ORG')
    if is_lead:
        if self.session.get('role') == 'leader':
            roles.append(u'<b>LEAD</b>')
        else:
            roles.append(u'LEAD')
    if is_memb:
        if self.session.get('role') == 'member':
            roles.append(u'<b>MEM</b>')
        else:
            roles.append(u'MEM')
    return roles


def create_roles(is_org, is_lead, is_memb):
    """Returns list of registered user roles for choosing current role"""
    roles = []
    cur_role_local = 'anonim'
    if is_org:
        roles.append(u'ORG')
        cur_role_local = 'organizer'
    if is_lead:
        roles.append(u'LEAD')
        cur_role_local = 'leader'
    if is_memb:
        roles.append(u'MEM')
        cur_role_local = 'member'
    return [roles, cur_role_local]
