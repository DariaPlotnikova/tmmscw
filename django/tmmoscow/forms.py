# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import defaults, models

Profile = get_user_model()


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, help_text=u'Логин')
    first_name = forms.CharField(max_length=50, help_text=u'Имя')
    last_name = forms.CharField(max_length=50, required=False, help_text=u'Фамилия')
    email = forms.EmailField(max_length=254,)
    qual = forms.ModelChoiceField(queryset=models.Qualification.objects.all(), help_text=u'Квалификация')
    birth = forms.IntegerField(help_text=u'Год рождения')

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'qual', 'birth', 'gender')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'qual', 'birth', 'gender')


class TeamForm(forms.ModelForm):

    class Meta:
        model = models.Team
        fields = ('title', 'location')
