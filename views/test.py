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
from views.common.base_handlers import BaseHandler


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
        org6 = Organizer(user=users.User('olishevskayaa@gmail.com'), nickname=u'Олишевская Анна',
                         contact='olishevskayaa@gmail.com')

        org2 = Organizer(user=users.User('test@example.com'), nickname=u'Тест Тестович', contact='test@example.com')

        org3 = Organizer(user=users.User('plotnikovanstu@gmail.com'), nickname=u'Плотникова Дарья',
                         contact='plotnikovanstu@gmail.com')

        org4 = Organizer(user=users.User('fordima1995@gmail.com'), nickname=u'Потапейко Дмитрий',
                         contact='fordima1995@gmail.com')

        org5 = Organizer(user=users.User('cyanat56@gmail.com'), nickname=u'Петров Никита', contact='cyanat56@gmail.com',
                         pass_to_edit='qwerty')

        lead1 = Leader(user=users.User('@gmail.com'), nickname=u'Олишевская Анна',
                       contact='anremonres@gmail.com', command=com2)

        lead2 = Leader(user=users.User('cyanat56@gmail.com'), nickname=u'Петров Никита',
                       contact='cyanat56@gmail.com', command=com1)

        memb1 = Member(user=users.User('plotnikovanstu@gmail.com'), pass_to_edit=paswd, sex=u'Женский',
                       nickname='plotnikovanstu@gmail.com',
                       surname=u'Плотникова Дарья',
                       command=com1, birthdate=1994, qualification='I')

        memb2 = Member(user=users.User('mar@h.n'), pass_to_edit=paswd, sex=u'Мужской', nickname='mar@h.n',
                       surname=u'Хайруллин Марат', command=com1,
                       birthdate=1994, qualification='I')

        memb3 = Member(user=users.User('fordima1995@gmail.com'), pass_to_edit=paswd, sex=u'Мужской',
                       nickname='fordima1995@gmail.com',
                       surname=u'Потапейко Дмитрий',
                       command=com2, birthdate=1995, qualification='I')

        memb4 = Member(user=users.User('cyanat56@gmail.com'), pass_to_edit=paswd, sex=u'Мужской',
                       nickname='cyanat56@gmail.com',
                       surname=u'Петров Никита',
                       command=com2, birthdate=1998, qualification='I')
        memb1.put()
        memb2.put()
        memb3.put()
        memb4.put()
        org1.put()
        org2.put()
        org3.put()
        org4.put()
        org5.put()
        org6.put()
        lead1.put()
        lead2.put()
        temp_values = {"membs": Member.all(),
                       "leads": Leader.all(),
                       "orgs": Organizer.all()}
        self.response.write(main.jinja_env.get_template('/tmmscw/test.html').render(temp_values))

    def post(self):
        pass  # TODO create handler as kanban in Brama (if kind='')


class Test(webapp2.RequestHandler):
    """
    Test handler for different purposes
    """

    def get(self):
        cur_user = users.get_current_user()
        # cur_lead = db.Query(Leader).filter('user =', cur_user).get()
        # user_members = db.Query(Member).filter('leader =', cur_lead)
        # memInfos = MemInfo.all()
        # usrs = "MemInfo: " + str(db.Query(MemInfo).count())
        # usrs += " | DistInfo: " + str(db.Query(DistInfo).count())
        # usrs += " | Competition: " + str(db.Query(Competition).count())
        # usrs += " | Distance: " + str(db.Query(Distance).count())
        # usrs += " | Info: " + str(db.Query(Info).count())
        # tmp = ''
        # orgs = Organizer.all()
        # for org in orgs:
        #     tmp += org.contact + " _ "
        # usrs += " | ORGS contact: " + tmp
        temp_values = {'test_data': cur_user}
        self.response.write(main.jinja_env.get_template('/tmmscw/test.html').render(temp_values))

    def post(self):
        pass


class CleanUp(BaseHandler):
    """
    Cleans up all session data
    """

    def get(self):
        self.session['role'] = 'anonim'
        mems = Member.all()
        orgs = Organizer.all()
        leads = Leader.all()
        comps = Competition.all()
        comms = Command.all()
        for mem in mems:
            mem.delete()
        for org in orgs:
            org.delete()
        for lead in leads:
            lead.delete()
        for comp in comps:
            comp.delete()
        for comm in comms:
            comm.delete()
