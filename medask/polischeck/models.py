from django.db import models


class Polis(models.Model): # Модель страхового полиса, хранящая формат номера полиса вместо самого номера

    POLIS_TYPES = [
            ('OMS', 'OMS'),
            ('DMS', 'DMS'),
        ] # Доступные типы страховых полисов
    
    company = models.CharField(max_length=255) # Имя страховой компании
    num_regex = models.CharField(max_length=50) # Регулярное выражение,
                                                # для определения принадлежности полиса к компании по его номеру.
    polis_type = models.CharField(max_length=3, choices=POLIS_TYPES, default='OMS')
    BILLING = models.IntegerField(default=0) # Счетчик успешных запросов по данному формату (regexp) номера полисов
    not_found_search = models.IntegerField(default=0) # Счетчик НЕ успешных запросов (номер не найден в БД страх. комп.)
    
    def __str__(self):
        return self.company + ' ' + self.polis_type
