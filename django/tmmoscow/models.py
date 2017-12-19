# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc. All rights reserved.
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

import uuid
from datetime import datetime
from django.db import models
from . import defaults
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


class Competition(models.Model):
    title = models.CharField(u'Название', max_length=511)
    start_date = models.DateField(u'Дата начала')
    end_date = models.DateField(u'Дата окончания')
    entry_end_date = models.DateTimeField(u'Дата и время окончания предварительной заявки', null=True, blank=True)
    place = models.CharField(u'Центр соревнований', max_length=512, null=True, blank=True)
    place_x = models.FloatField(u'X координата центра соревнований', null=True, blank=True)
    place_y = models.FloatField(u'Y координата центра соревнований', null=True, blank=True)

    def is_open_entry(self):
        tz_info = self.entry_end_date.tzinfo
        return self.entry_end_date > datetime.now(tz=tz_info)

    def __unicode__(self):
        return u'%s  |  с %s по %s  |  %s ' % (self.title, self.start_date, self.end_date, self.place)

    class Meta:
        db_table = 'tm_competition'
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = 'start_date',


class Day(models.Model):
    competition = models.ForeignKey('tmmoscow.Competition', verbose_name=u'Соревнование', related_name='days')
    info = models.FileField(u'Техническая информация', blank=True, null=True)
    date = models.DateField(u'Дата')
    place = models.CharField(u'Расположение старта', max_length=512, null=True, blank=True)
    place_x = models.FloatField(u'X координата старта дисциплин', null=True, blank=True)
    place_y = models.FloatField(u'Y координата старта дисциплин', null=True, blank=True)
    tech_end_date = models.DateTimeField(u'Дата и время окончания подачи тенической заявки', null=True, blank=True)

    def tech_is_open(self):
        tz_info = self.tech_end_date.tzinfo
        return self.tech_end_date > datetime.now(tz_info)

    def __unicode__(self):
        return u'День %s  |  %s  |  %s ' % (self.date, self.competition.title, self.place)

    class Meta:
        db_table = 'tm_day'
        verbose_name = 'День соревнования'
        verbose_name_plural = 'Дни соревнований'
        ordering = 'date',


class Distance(models.Model):
    day = models.ForeignKey('tmmoscow.Day', verbose_name=u'День соревнования', related_name='distances')
    type = models.PositiveIntegerField(u'Тип дистанции', choices=defaults.DISCIPLINE_TYPES)
    is_long = models.BooleanField(u'Длинная', default=False, blank=True)
    length = models.FloatField(u'Длина')
    dclass = models.PositiveIntegerField(u'Класс дистанции', choices=defaults.DISTANCE_CLASSES, default=defaults.DC_1)
    climb = models.FloatField(u'Набор высоты', default=0, blank=True)
    stage_cnt = models.PositiveSmallIntegerField(u'Кол-во технических этапов', default=0, blank=True)
    point_cnt = models.PositiveSmallIntegerField(u'Кол-во контрольных пунктов', default=0, blank=True)
    groups = models.ManyToManyField('tmmoscow.Group', verbose_name=u'Допустимые группы', related_name='distances')
    quals = models.ManyToManyField('tmmoscow.Qualification', verbose_name=u'Допустимые разряды', related_name='distances')

    def __unicode__(self):
        return u'%s - %s (%s км)' % (self.dclass, self.get_long(), self.length)

    def get_long(self):
        return u'длинная' if self.is_long else u'короткая'

    def get_groups_str(self):
        return ', '.join([gr.title for gr in self.groups.all()])

    def get_quals_str(self):
        return ', '.join([q.title for q in self.quals.all()])

    def get_specials_str(self):
        return ', '.join(['%s - %s' % (sg.group.title, sg.qual.title) for sg in self.special_groups.all()])

    class Meta:
        db_table = 'tm_distance'
        verbose_name = 'Дистанция дня'
        verbose_name_plural = 'Дистанции дней'


class SpecialGroup(models.Model):
    """ Эта модель для особых пар группа-разряд,
    которые могут позволить например, 16-ти летнему с
    разрядом МС участвовать на 5м классе """
    group = models.ForeignKey('tmmoscow.Group', verbose_name=u'Группа', related_name='specials')
    qual = models.ForeignKey('tmmoscow.Qualification', verbose_name=u'Разряд', related_name='specials')
    distance = models.ForeignKey('tmmoscow.Distance', verbose_name=u'Дистанция', related_name='special_groups')

    def __unicode__(self):
        return '%s - %s' % (self.group.title, self.qual.title)

    class Meta:
        db_table = 'tm_specialgroup'
        verbose_name = u'Особая группа-разряд'
        verbose_name_plural = u'Особые группы-разряды'


class Group(models.Model):
    title = models.CharField(u'Название группы', max_length=127)
    year_from = models.IntegerField(u'Год с')
    year_to = models.IntegerField(u'Год по')
    sex = models.PositiveIntegerField(u'Пол участников', choices=defaults.MEMBER_SEXES)

    def __unicode__(self):
        return '%s  |  с %s по %s  |  %s' % (self.title, self.year_from, self.year_to, self.get_sex_display())

    class Meta:
        db_table = 'tm_group'
        verbose_name = 'Возрастная группа'
        verbose_name_plural = 'Возрасные группы'


class Qualification(models.Model):
    title = models.CharField(u'Название', max_length=127)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'tm_qualification'
        verbose_name = 'Разряд'
        verbose_name_plural = 'Разряды'


class TmUser(AbstractUser):
    uniq_id = models.UUIDField(u'Уникальный ID', default=uuid.uuid4, editable=False)
    birth = models.IntegerField(u'Год рождения', blank=True, null=True)
    qual = models.ForeignKey(Qualification, verbose_name=u'Разряд', related_name='users', blank=True, null=True)
    edit_pass = models.CharField(u'Пароль редактирования', max_length=16, blank=True, default='123456')
    is_leader = models.BooleanField(u'Руководитель', default=True, blank=True)
    is_org = models.BooleanField(u'Организатор', default=False, blank=True)
    is_active = models.BooleanField(u'Активный', default=True, blank=True)

    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def is_member(self):
        return not self.is_leader and not self.is_org

    def get_members(self):
        return 0

    def chip(self):
        return '-'

    def get_teams(self):
        return [uc.team for uc in self.teams.order_by('is_leader')]

    def create_team(self):
        team = Team.objects.create(title=u'Лично (%s)' % self.name(),)
        UserCommand.objects.create(team=team, member=self, is_leader=True)
        return team

    def get_my_team(self):
        return self.teams.filter(is_leader=True)[0].team if self.teams.count() else None

    class Meta(AbstractUser.Meta):
        abstract = False
        db_table = 'tm_user'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'


class Team(models.Model):
    title = models.CharField(u'Название', max_length=256)
    location = models.CharField(u'Территория', max_length=512, blank=True, null=True)
    geo_x = models.CharField(u'X-координата', max_length=16, blank=True, null=True)
    geo_y = models.CharField(u'Y-координата', max_length=16, blank=True, null=True)

    def is_leader(self, user):
        return user in [lead.member for lead in self.members.filter(is_leader=True)]

    def get_members(self):
        return [uc.member for uc in self.members.filter(is_in_team=True, is_leader=False)]

    def get_leaders(self):
        return [lead.member for lead in self.members.filter(is_leader=True)]

    def get_users_requests(self):
        return [uc.member for uc in self.members.filter(is_in_team=False, is_leader=False)]

    def to_json(self):
        return {
            'id': self.pk,
            'title': self.title,
            'lead': ', '.join([l.name() for l in self.get_leaders()]),
            'location': self.location
        }

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.location)

    class Meta:
        db_table = 'tm_team'
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'


class UserCommand(models.Model):
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='members')
    is_leader = models.BooleanField(u'Является руководителем', blank=True, default=False)
    is_in_team = models.BooleanField(u'В команде', blank=True, default=False)
    member = models.ForeignKey(TmUser, verbose_name=u'Участик', related_name='teams', null=True)

    def __unicode__(self):
        return ' '.join([self.team.title, self.member.name()])

    class Meta:
        db_table = 'tm_user_team'
        verbose_name = u'Команда-Участник'
        verbose_name_plural = u'Команда-участники'
