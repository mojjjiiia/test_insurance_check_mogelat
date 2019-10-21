from rest_framework import serializers
from .models import Polis


class PolisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polis
        fields = ('company_name', 'polis_type', 'num_regex')
