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

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from tmmoscow.views import index, competition, add_to_competition, signup, edit_profile, \
    my_team, select_team, user_roles, profile, check_team_exist, to_team, add_to_distances

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^competition/(?P<comp_pk>\d+)/$', competition, name='competition'),
    url(r'^competition/add/members/(?P<comp_pk>\d+)/$', add_to_competition, name='competition-add-to'),
    url(r'^competition/add/distances/(?P<comp_pk>\d+)/$', add_to_distances, name='distances-add-to'),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/signup/$', signup, name='signup'),
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^accounts/edit/(?P<user_pk>\d+)/$', edit_profile, name='profile-edit'),
    url(r'^accounts/edit/team/(?P<team_pk>\d+)/$', my_team, name='my-team'),
    url(r'^accounts/edit/(?P<user_pk>\d+)/roles/$', user_roles, name='roles'),
    url(r'^accounts/edit/(?P<user_pk>\d+)/selectteam/$', select_team, name='select-team'),

    url(r'^accounts/toteam/$', to_team, name='to-team'),

    url(r'^api/check_team_exist/$', check_team_exist, name='check-team'),

    url(r'^admin/', include(admin.site.urls)),
]
