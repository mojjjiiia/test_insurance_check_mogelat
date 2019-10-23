from django.db import models


class Polis(models.Model):
    
    POLIS_TYPES = [
            ('OMS', 'OMS'),
            ('DMS', 'DMS'),
        ]
    
    company = models.CharField(max_length=255)
    num_regex = models.CharField(max_length=50)
    polis_type = models.CharField(max_length=3, choices=POLIS_TYPES, default='OMS')
    BILLING = models.IntegerField(default=0)
    not_found_search = models.IntegerField(default=0)
    
    def __str__(self):
        return self.company + ' ' + self.polis_type


