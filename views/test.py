# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import db

import main
from models.competition import MemInfo, DistInfo, Competition, Distance, Info
from models.visitor import Organizer, Leader, Member, Command
from views.utils import salt_pass


class Db(webapp2.RequestHandler):
    """
    Fill in initial data in database
    """
    def get(self):
        """(for developing mode) Adds initial data to database"""
        user = users.get_current_user()
        com1 = Command(name=u'Фортуна', territory=u'Ангарск')
        com2 = Command(name=u'Фортуна', territory=u'Москва')
        com1.put()
        com2.put()
        paswd = '123'
        paswd = salt_pass(paswd)
        org1 = Organizer(user=users.User('anremonres@gmail.com'), nickname=u'Олишевская Анна',
                         contact='anremonres@gmail.com')
        org2 = Organizer(user=users.User('test@example.com'), nickname=u'Тест Тестович', contact='test@example.com')
        org3 = Organizer(user=users.User('plotnikovanstu@gmail.com'), nickname=u'Плотникова Дарья',
                         contact='plotnikovanstu@gmail.com')
        org4 = Organizer(user=users.User('fordima1995@gmail.com'), nickname=u'Потапейко Дмитрий',
                         contact='fordima1995@gmail.com')
        lead1 = Leader(user=users.User('anremonres@gmail.com'), nickname=u'Олишевская Анна',
                       contact='anremonres@gmail.com', command=com2)

        memb1 = Member(pass_to_edit=paswd, sex=u'Женский', nickname='plotnikovanstu@gmail.com',
                       surname=u'Плотникова Дарья',
                       command=com1, birthdate=1994, qualification='I')
        memb2 = Member(pass_to_edit=paswd, sex=u'Мужской', nickname='mar@h.n', surname=u'Хайруллин Марат', command=com1,
                       birthdate=1994, qualification='I')
        memb3 = Member(pass_to_edit=paswd, sex=u'Мужской', nickname='fordima1995@gmail.com',
                       surname=u'Потапейко Дмитрий',
                       command=com2, birthdate=1995, qualification='I')
        memb1.put()
        memb2.put()
        memb3.put()
        org1.put()
        org2.put()
        org3.put()
        org4.put()
        lead1.put()

    def post(self):
        pass            # TODO create handler as kanban in Brama (if kind='')


class Test(webapp2.RequestHandler):
    """
    Test handler for different purposes
    """
    def get(self):
        cur_user = users.get_current_user()
        #cur_lead = db.Query(Leader).filter('user =', cur_user).get()
        #user_members = db.Query(Member).filter('leader =', cur_lead)
        #memInfos = MemInfo.all()
        #usrs = "MemInfo: " + str(db.Query(MemInfo).count())
        #usrs += " | DistInfo: " + str(db.Query(DistInfo).count())
        #usrs += " | Competition: " + str(db.Query(Competition).count())
        #usrs += " | Distance: " + str(db.Query(Distance).count())
        #usrs += " | Info: " + str(db.Query(Info).count())
        #tmp = ''
        #orgs = Organizer.all()
        #for org in orgs:
        #    tmp += org.contact + " _ "
        #usrs += " | ORGS contact: " + tmp
        temp_values = {'test_data': cur_user}
        self.response.write(main.jinja_env.get_template('/tmmscw/test.html').render(temp_values))

    def post(self):
        pass



class Layout(webapp2.RequestHandler):
    """
    Layout for general purposes
    """
    def get(self):
        template = '/tmmscw/layout.html'
        temp_values = dict()
        self.response.write(main.jinja_env.get_template(template).render(temp_values))

    def post(self):
        pass