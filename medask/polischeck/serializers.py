from rest_framework import serializers
from .models import Polis


class PolisSerializer(serializers.Serializer): # Сериализатор для данных полученных из формы
    choices = [('OMS', 'OMS'), ('DMS', 'DMS')]
    
    company = serializers.CharField(max_length = 255) # Имя компании
    number = serializers.CharField(max_length = 50) # Номер полиса
    polis_type = serializers.ChoiceField(choices) # Тип полиса

    
class NotFoundPolisSerializer(serializers.ModelSerializer): # Сериализатор для моделей из локальной базы (с регулярками)
    class Meta:
        model = Polis
        fields = ['company', 'num_regex', 'polis_type']
