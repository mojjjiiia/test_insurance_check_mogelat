from rest_framework import serializers
from .models import Polis


class PolisSerializer(serializers.Serializer):
    choices = [('OMS', 'OMS'), ('DMS', 'DMS')]
    
    company = serializers.CharField(max_length = 255)
    number = serializers.CharField(max_length = 50)
    polis_type = serializers.ChoiceField(choices)

    
class NotFoundPolisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polis
        fields = ['company', 'num_regex', 'polis_type']
        
