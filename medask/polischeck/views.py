from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import num_check, service_check, num_to_regex, request_to_sk
from .serializers import PolisSerializer, NotFoundPolisSerializer
from urllib.parse import unquote_plus


class PolisCheckView(APIView):
    def get(self, request):
        number = request.GET.get('number', None)
        service = request.GET.get('service', None)
# Если в GET запросе указан параметр number, проверяет в локальной БД формата номера полиса
# Вернется имя компании и тип полиса
        if number:
            resp = {}
            try:
                resp['company'], resp['polis_type'], polis = num_check(unquote_plus(number))
                return Response(resp)
            except ObjectDoesNotExist:
                return Response('Not in local database', status=404)
# Если в GET запросе указан параметр service, проверяет в БД СК наличие услуги (доступной и недоступной)
# Вернет True или False (если отстуствует в БД)
        if service:
            service = unquote_plus(service)
            in_database = service_check(service)
            return Response({'service_in_base': in_database})
        return Response("EMPTY REQUEST") # При пустом GET запросе

    def post(self, request):
# При POST запросе вернет JSON с данными от СК о полисе и доступности услуг.
        serializer = PolisSerializer(data=request.data)
        if serializer.is_valid(): # Проверка данных формы из запроса
            try:
                polis = num_check(request.data['number'])[-1] # поиск инстанса модели из локальной БД
            except ObjectDoesNotExist:
# Если инстанс не найден создаем новый инстанс с новой регуляркой
                regex = num_to_regex(request.data['number'])
                nf_serializer = NotFoundPolisSerializer(data={'company':request.data['company'],
                                                        'num_regex': regex,
                                                        'polis_type': request.data['polis_type']})
                if nf_serializer.is_valid():
                    polis = nf_serializer.save()
                else:
                    return Response(nf_serializer.errors)

            try:
# Производим запрос к БД СК
                resp = request_to_sk(**serializer.validated_data, services=request.data['services'])
                polis.BILLING += 1 # Увеличиваем счетчик успешных запросов по данной регулярке
                polis.save()
                return Response(resp)
            except ObjectDoesNotExist:
                polis.not_found_search += 1 # Полис в БД СК не найден - увеличиваем счетчик неудачных запросов
                polis.save()
                raise Http404
            except Http404:
# Если из формы ,по каким-то причинам, получили неверное имя компании, возвращаем сообщение об этом
                return Response({'Company': 'WRONG COMPANY NAME!'}, status=404)

        else:
            return Response(serializer.errors) # Возврат ошибок, если поля формы заполнены неправильно
