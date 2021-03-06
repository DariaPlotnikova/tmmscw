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

import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Competition, Team, UserCommand, Distance, UserDistance
from .forms import SignUpForm, ProfileForm, TeamForm

Profile = get_user_model()


def index(request):
    """ Главная страница, список соревнований """
    template_name = 'tmmoscow/index.html'
    comps = Competition.objects.all()
    return render(request, template_name, dict(comps=comps))


def competition(request, comp_pk):
    """ Подробности о соревновании """
    template_name = 'tmmoscow/competition.html'
    competition = Competition.objects.get(pk=comp_pk)
    return render(request, template_name, dict(comp=competition))


def signup(request):
    """ Регистрирует участника и создает его команду """
    message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user.create_team()
            return redirect('index')
        message = form.errors
        print message
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', dict(form=form, message=message))


@login_required
def add_to_competition(request, comp_pk):
    """ Открывает страницу выбора участников для регистрации на соревновании """
    template_name = 'tmmoscow/add_to_competition.html'
    competition = Competition.objects.get(pk=comp_pk)
    return render(request, template_name, dict(comp=competition, user=request.user))


@login_required
def add_to_distances(request, comp_pk):
    """ Открывает страницу выбора участников для распределения по дистанциям """
    template_name = 'tmmoscow/add_to_distances.html'
    competition = Competition.objects.get(pk=comp_pk)
    team = request.user.get_my_teams()[0]
    if request.method == 'GET':
        members = request.GET.getlist('members')
        members = Profile.objects.filter(pk__in=members)
        return render(request, template_name, dict(comp=competition, user=request.user, members=members))
    else:
        members = request.POST.get('members').split(',')
        for memb_pk in members:
            distances = request.POST.getlist('member_%s' % memb_pk)
            if distances:
                member = Profile.objects.get(pk=memb_pk)
                distances = Distance.objects.filter(pk__in=distances)
                for dist in distances:
                    UserDistance.objects.create(user=member, distance=dist, team=team)
        return redirect('/')


def member_list(request, comp_pk):
    """ Список участников, заявленный на соревнование """
    template_name = 'tmmoscow/member_list.html'
    competition = Competition.objects.prefetch_related().get(pk=comp_pk)
    return render(request, template_name, dict(comp=competition))


@login_required
def edit_profile(request, user_pk):
    """ Редактирование профиля пользователя """
    template_name = 'profile/edit.html'
    message = ''
    user = get_object_or_404(Profile, pk=user_pk)
    if user == request.user:
        form = ProfileForm(request.POST, instance=user)
        if request.POST:
            if form.is_valid():
                user = form.save()
            else:
                message = form.errors
        form = ProfileForm(instance=user)
        return render(request, template_name, dict(form=form, user=form.instance, message=message))
    else:
        raise Http404


@login_required
def my_team(request, team_pk):
    """ Редактирование команды ее руководителем """
    template_name = 'profile/team.html'
    message = ''
    team = get_object_or_404(Team, pk=team_pk)
    if team.is_leader(request.user):
        if request.method == 'POST':
            form = TeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
            else:
                message = form.errors
        form = TeamForm(instance=team)
        return render(request, template_name, dict(form=form, team=form.instance, message=message))
    else:
        raise Http404


@login_required
def user_roles(request, user_pk):
    """ Список ролей пользователя в системе """
    template_name = 'profile/roles.html'
    message = ''
    user = get_object_or_404(Profile, pk=user_pk)
    if user == request.user:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            else:
                message = form.errors
        form = ProfileForm(instance=user)
        return render(request, template_name, dict(form=form, user=form.instance, message=message))
    else:
        raise Http404


@login_required
def select_team(request, user_pk):
    template_name = 'profile/select_team.html'
    message = ''
    user = get_object_or_404(Profile, pk=user_pk)
    if user == request.user:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            else:
                message = form.errors
        form = ProfileForm(instance=user)
        return render(request, template_name, dict(user=form.instance, message=message))
    else:
        raise Http404


@login_required
def profile(request):
    """ Страница пользователя, Личный кабинет """
    template_name = 'profile/profile.html'
    user = request.user
    if user is not None:
        return render(request, template_name, dict(user=user))
    else:
        raise Http404


@login_required
def check_team_exist(request):
    """ Проверяет, существует ли команда по названию и территории """
    team_name = request.GET.get('title', '').strip()
    team_location = request.GET.get('location', '').strip()
    teams = Team.objects.filter(title=team_name, location=team_location)
    return HttpResponse(json.dumps(
        {'status': 'success', 'teams_cnt': teams.count(), 'teams': [t.to_json() for t in teams]}),
        content_type='application/json')


@login_required
def to_team(request):
    """ Отправляет заявку участника на добавление в команду и подтверждает ее со стороны руководителя """
    team = get_object_or_404(Team, pk=request.POST.get('team'))
    member = get_object_or_404(Profile, pk=request.POST.get('member'))
    if member not in team.get_members() and member not in team.get_users_requests():    # отправка заявки
        uc = UserCommand.objects.create(team=team, member=member, is_in_team=False)
        return redirect(resolve_url('select-team', request.user.pk))
    else:   # подтверждение заявки
        uc = UserCommand.objects.get(team=team, member=member)
        uc.is_in_team = True
        uc.save()
        return HttpResponse(json.dumps({'status': 'success', 'message': u'Пользователь включен в команду'}))
