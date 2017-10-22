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

from django.contrib import admin

from .models import Competition, Day, Distance, Group, Qualification, SpecialGroup


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'place')


class DayAdmin(admin.ModelAdmin):
    list_display = ('competition', 'date', 'place', 'tech_end_date')


class SpecialInline(admin.StackedInline):
    model = SpecialGroup
    extra = 2
    verbose_name = u'Особые группы-разряды'


class DistanceAdmin(admin.ModelAdmin):
    list_display = ('day_display', 'competition_display', 'type_display', 'dclass',
              'stage_cnt', 'point_cnt', 'groups_display',
              'quals_display', 'specials_display')
    inlines = [SpecialInline]

    def day_display(self, obj):
        return obj.day.date
    day_display.short_description = u'Дата'

    def competition_display(self, obj):
        return obj.day.competition.title
    competition_display.short_description = u'Соревнование'

    def type_display(self, obj):
        return '%s - %s' % (obj.get_type_display(), u'длинная' if obj.is_long else u'короткая')
    type_display.short_description = u'Дисциплина'

    def groups_display(self, obj):
        return ', '.join([gr.title for gr in obj.groups.all()])
    groups_display.short_description = u'Допустимые группы'

    def quals_display(self, obj):
        return ', '.join([q.title for q in obj.quals.all()])
    quals_display.short_description = u'Допустимые разряды'

    def specials_display(self, obj):
        return ', '.join(unicode(sp) for sp in obj.special_groups.all()) if obj.special_groups else '-'
    specials_display.short_description = u'Особые группы-разряды'

class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_from', 'year_to', 'sex')


class QualificationAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Distance, DistanceAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Qualification, QualificationAdmin)
