# -*- coding: utf-8 -*-
import datetime
from django import template
from django.contrib.auth import get_user_model
from tmmoscow.models import Distance

register = template.Library()
Profile = get_user_model()


@register.simple_tag
def can_go_to_dist(memb, dist):
    """ Проверяет, может ли участник принимать участие в дистанции """
    return memb.can_participate_in_dist(dist)

@register.simple_tag
def can_go_to_competition(memb, comp):
    """ Проверяет, может ли участник принимать участие во всём соревновании """
    return memb.can_participate_in(comp)