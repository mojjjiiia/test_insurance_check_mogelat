from django.db import models
import django.core.exceptions
import re

class Polis(models.Model):
    
    POLIS_TYPES = 
        [
            ('OMS', 'OMS'),
            ('DMS', 'DMS'),
        ]
    
    company_name = models.CharField(max_length=255)
    num_regex = models.CharField(max_length=50)
    polis_type = models.CharField(max_length=3, choices=POLIS_TYPES, default='OMS')    
    
    def __str__(self):
        return self.company_name

def num_check(number):
    
    polises = Polis.objects.all()
    for polis in polises:
        if re.match(polis.num_regex, number):
            company = polis.company_name
            polis_type = polis.polis_type
            return company, polis_type
    
    raise ObjectDoesNotExist
