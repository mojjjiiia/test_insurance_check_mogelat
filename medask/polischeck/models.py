from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re
import os
import json


class Polis(models.Model):
    
    POLIS_TYPES = [
            ('OMS', 'OMS'),
            ('DMS', 'DMS'),
        ]
    
    company_name = models.CharField(max_length=255)
    num_regex = models.CharField(max_length=50)
    polis_type = models.CharField(max_length=3, choices=POLIS_TYPES, default='OMS')    
    
    def __str__(self):
        return self.company_name + ' ' + self.polis_type


def num_check(number):
    
    polises = Polis.objects.all()
    for polis in polises:
        if re.match(polis.num_regex, number):
            company = polis.company_name
            polis_type = polis.polis_type
            return company, polis_type
    
    raise ObjectDoesNotExist


def service_check(service):
    table_path = '/'.join([os.path.dirname(__file__), '../tables/services.json'])
    with open(table_path, 'r', encoding='UTF-8') as services_json:
        all_services = json.load(services_json)
    for column in all_services:
        if service in all_services[column]:
            return True
        
    raise ObjectDoesNotExist
