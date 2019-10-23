from rest_framework import serializers
from .models import Polis


class PolisSerializer(serializers.Serializer):
    choices = [('OMS', 'OMS'), ('DMS', 'DMS')]
    
    company = serializers.CharField(max_length = 255)
    polis_number = serializers.CharField(max_length = 50) 
    polis_type = serializers.ChoiceField(choices)
    services = serializers.CharField(max_length = 255)     
