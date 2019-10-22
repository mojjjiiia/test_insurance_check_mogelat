from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re
import os
import json
#Для перевода даты из json в формат DateTime использую Dateutil pip3 install python-dateutil
from dateutil import parser


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
    return False

def request_to_sk(company, number, polis_type):
    companies_table = '/'.join([os.path.dirname(__file__), '../tables/companies_data.json'])
    
    with open(companies_table, 'r', encoding='UTF-8') as companies_json:
        companies_from_db = json.load(companies_json)
        
    try:
        for polis in companies_from_db[company]:
            if polis_type == polis['type'] and number == polis['number']:
                polis_ltd_sk = company
                polis_ltd_type = polis['type']
                polis_ltd_id = polis['number']
                polis_ltd_date_end = parser.parse(polis['due_date']) #datetime.datime
                polis_ltd_tel = polis['phone']
    except KeyError:
        raise ObjectDoesNotExist
    
    try:
        return polis_ltd_sk, polis_ltd_type, polis_ltd_id, polis_ltd_date_end, polis_ltd_tel
    except NameError:
        raise ObjectDoesNotExist
            
            
        
        
        
        
        
        
        
