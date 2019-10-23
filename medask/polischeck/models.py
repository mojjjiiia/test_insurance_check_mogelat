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
    BILLING = models.IntegerField(default=0)
    not_found_search = models.IntegerField(default=0)
    
    def __str__(self):
        return self.company_name + ' ' + self.polis_type
    

class LocalBase(models.Model):
    polis_ltd_prefix = models.CharField(max_length=50) #Regexp для ненайденных номеров полисов
    local_polis_search = models.IntegerField(default=0)
    polis_ltd_datetime = models.DateTimeField(auto_now_add=True)
    #auto_now_add=True для того что бы оценить количество обращений по данному регулярному выражению и дату первого обращения   


def num_check(number):
    polises = Polis.objects.all()
    for polis in polises:
        if re.match(polis.num_regex, number):
            company = polis.company_name
            polis_type = polis.polis_type
            return company, polis_type, polis
    
    raise ObjectDoesNotExist



def service_check(service):
    table_path = '/'.join([os.path.dirname(__file__), '../tables/services.json'])
    with open(table_path, 'r', encoding='UTF-8') as services_json:
        all_services = json.load(services_json)

    for column in all_services:
        if service.lower() in [i.lower() for i in column]:
            return True
    return False


def request_to_sk(company, number, polis_type, services):
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
    (
        polis_ltd_inservice, 
        polis_ltd_notservice, 
        polis_ltd_notfoundservice
    ) = request_to_service_db(services)
    return {
        'polis_ltd_sk': polis_ltd_sk,  
        'polis_ltd_type': polis_ltd_type, 
        'polis_ltd_id': polis_ltd_id, 
        'polis_ltd_date_end': polis_ltd_date_end, 
        'polis_ltd_tel': polis_ltd_tel,
        'polis_ltd_inservice': polis_ltd_inservice, 
        'polis_ltd_notservice': polis_ltd_notservice, 
        'polis_ltd_notfoundservice': polis_ltd_notfoundservice,
    }
    
    #try:
    #    return polis_ltd_sk, polis_ltd_type, polis_ltd_id, polis_ltd_date_end, polis_ltd_tel
    #except NameError:
    #    raise ObjectDoesNotExist
       

def request_to_service_db(services):
    polis_ltd_inservice = []
    polis_ltd_notservice = []
    polis_ltd_notfoundservice = []
    
    table_path = '/'.join([os.path.dirname(__file__), '../tables/services.json'])
    with open(table_path, 'r', encoding='UTF-8') as services_json:
        services_db = json.load(services_json)
        
    for service in services:
        if service.lower() in [i.lower() for i in services_db['inservice']]:
            polis_ltd_inservice.append(service)

        elif service.lower() in [i.lower() for i in services_db['outservice']]:
            polis_ltd_notservice.append(service)

        else:
            polis_ltd_notfoundservice.append(service)
            
    return polis_ltd_inservice, polis_ltd_notservice, polis_ltd_notfoundservice

def num_to_regex(number):
    regex = ''
    for i in ['\d' if i.isdigit() else i for i in number]:
        regex += i
    return regex
