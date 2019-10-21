from rest_framework import serializers

class PolisSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    num_regex = serializers.CharField(max_length=50)
    polis_type = serializers.CharField(max_length=3)
