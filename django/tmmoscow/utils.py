# -*- coding: utf-8 -*-
import csv
from . import models


def generate_competition_csv(response, competition):
    """ Формирует csv-файл для экспорта заявленных участников в Excel """
    distances = competition.get_distances()
    members = models.UserDistance.objects.filter(distance__in=distances).order_by('distance')
    writer = csv.writer(response)
    for memb in members:
        writer.writerow([memb.user.name(), memb.user.birth])


