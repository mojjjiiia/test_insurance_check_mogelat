from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Polis
import re
import os
import json
# Для перевода даты из json в формат DateTime использую Dateutil pip3 install python-dateutil
from dateutil import parser


def num_check(number):
    polises = Polis.objects.all()
    for polis in polises:
        if re.match(polis.num_regex, number):
            company = polis.company
            polis_type = polis.polis_type
            return company, polis_type, polis

    raise ObjectDoesNotExist


def service_check(service):
    table_path = '/'.join([os.path.dirname(__file__), '../tables/services.json'])
    with open(table_path, 'r', encoding='UTF-8') as services_json:
        all_services = json.load(services_json)

    for column in all_services:
        if service.lower() in [i.lower() for i in all_services[column]]:
            return True
    return False


def request_to_sk(company, number, polis_type, services):
    companies_table = '/'.join([os.path.dirname(__file__), '../tables/companies_data.json'])

    with open(companies_table, 'r', encoding='UTF-8') as companies_json:
        companies_from_db = json.load(companies_json)
    try:
        for polis in companies_from_db[company.upper()]:
            if polis_type == polis['type'] and number == polis['number']:
                polis_ltd_sk = company
                polis_ltd_type = polis['type']
                polis_ltd_id = polis['number']
                polis_ltd_date_end = parser.parse(polis['due_date'])  # datetime.datime
                polis_ltd_tel = polis['phone']
                (
                    polis_ltd_inservice,
                    polis_ltd_notservice,
                    polis_ltd_notfoundservice
                ) = request_to_service_db(services)
                return {
                    'polis_ltd_sk': polis_ltd_sk,
                    'polis_ltd_type': polis_ltd_type,
                    'polis_ltd_id': polis_ltd_id,
                    'polis_ltd_date_end': polis_ltd_date_end.strftime('%d.%m.%Y'),
                    'polis_ltd_tel': polis_ltd_tel,
                    'polis_ltd_inservice': polis_ltd_inservice,
                    'polis_ltd_notservice': polis_ltd_notservice,
                    'polis_ltd_notfoundservice': polis_ltd_notfoundservice,
                }

        raise ObjectDoesNotExist
    except KeyError:
        raise Http404


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
    regex += '$'
    return regex
