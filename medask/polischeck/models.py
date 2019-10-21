from django.db import models

class Polis(models.Model):
    
    POLIS_TYPES = 
        [
            ('OMS', 'OMS'),
            ('DMS', 'DMS'),
        ]
    
    company_name = models.CharField(max_length=255)
    num_regex = models.CharField(max_length=50)
    polis_type = models.CharField(max_length=3, choices=POLIS_TYPES, default='OMS')
    
