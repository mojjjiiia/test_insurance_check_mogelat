from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import num_check, service_check, request_to_sk, request_to_service_db
from .serializers import PolisSerializer
from urllib.parse import unquote_plus
import json


class PolisCheckView(APIView):
    def get(self, request):
        number = request.GET.get('number', None)
        service = request.GET.get('service', None)

        if number:
            resp = {}
            try:
                resp['company'], resp['polis_type'] = num_check(unquote_plus(number))
                return Response(resp)
            except ObjectDoesNotExist:
                return Response(resp)

        if service:
            service = unquote_plus(service)
            in_database = service_check(service)
            return Response({'service_in_base': in_database})

    def post(self, request):
        #company = request.data['company']
        #polis_number = request.data['polis_number']
        #polis_type = request.data['polis_type']
        #services = request.data['services']
        
        serializer = PolisSerializer(request.data)
        if serializer.is_valid():
            try:
            #(
            #    polis_ltd_sk,
            #    polis_ltd_type,
            #    polis_ltd_id,
            #    polis_ltd_date_end,
            #    polis_ltd_tel,
            #    polis_ltd_inservice,
            #    polis_ltd_notservice,
            #    polis_ltd_notfoundservice,
            #) = request_to_sk(serializer.validated_data)
                return Response(request_to_sk(serializer.validated_data))
            except ObjectDoesNotExist:
                raise Http404
        #(
        #    polis_ltd_inservice,
        #    polis_ltd_notservice,
        #    polis_ltd_notfoundservice,
        #) = request_to_service_db(services)

        #    return Response(
        #        {
        #             'polis_ltd_sk': polis_ltd_sk,
        #             'polis_ltd_type': polis_ltd_type,
        #             'polis_ltd_id': polis_ltd_id,
        #             'polis_ltd_date_end': polis_ltd_date_end.strftime('%d.%m.%y'),
        #             'polis_ltd_tel': polis_ltd_tel,
        #             'polis_ltd_inservice': polis_ltd_inservice,
        #             'polis_ltd_notservice': polis_ltd_notservice,
        #             'polis_ltd_notfoundservice': polis_ltd_notfoundservice,
        #        }
        #    )
        else:
            return Response(serializer.errors)
