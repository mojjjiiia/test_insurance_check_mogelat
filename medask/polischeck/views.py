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

        if number:
            resp = {}
            try:
                resp['company'], resp['polis_type'], polis = num_check(unquote_plus(number))
                return Response(resp)
            except ObjectDoesNotExist:
                return Response(resp)

        if service:
            service = unquote_plus(service)
            in_database = service_check(service)
            return Response({'service_in_base': in_database})

    def post(self, request):
        
        serializer = PolisSerializer(data=request.data)
        if serializer.is_valid():     
            try:
                polis = num_check(request.data['number'])[-1]
            except ObjectDoesNotExist:
                regex = num_to_regex(request.data['number'])
                nf_serializer = NotFoundPolisSerializer(data={'company':request.data['company'],
                                                        'num_regex': regex,
                                                        'polis_type': request.data['polis_type']})
                if nf_serializer.is_valid():
                    polis = nf_serializer.save()
                else:
                    return Response(nf_serializer.errors)

            try:
                resp = request_to_sk(**serializer.validated_data, services=request.data['services'])
                polis.BILLING += 1
                polis.save()
                return Response(resp)
            except ObjectDoesNotExist:
                polis.not_found_search += 1
                polis.save()
                raise Http404
            except Http404:
                return Response({'Company': 'WRONG NAME!'}, status=404)

        else:
            return Response(serializer.errors)
