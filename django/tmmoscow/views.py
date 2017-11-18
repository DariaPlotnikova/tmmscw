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

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Competition, Team
from .forms import SignUpForm, ProfileForm, TeamForm


Profile = get_user_model()


def index(request):
    template_name = 'tmmoscow/index.html'
    comps = Competition.objects.all()
    return render(request, template_name, dict(comps=comps))


def competition(request, comp_pk):
    template_name = 'tmmoscow/competition.html'
    competition = Competition.objects.get(pk=comp_pk)
    return render(request, template_name, dict(comp=competition))


def signup(request):
    message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        message = form.errors
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', dict(form=form, message=message))


@login_required
def add_to_competition(request, comp_pk):
    template_name = 'tmmoscow/add_to_competition.html'
    competition = Competition.objects.get(pk=comp_pk)
    return render(request, template_name, dict(comp=competition))


@login_required
def edit_profile(request, user_pk):
    template_name = 'profile/edit.html'
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
def my_team(request, team_pk):
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
        return render(request, template_name, dict(form=form, user=form.instance, message=message))
    else:
        raise Http404