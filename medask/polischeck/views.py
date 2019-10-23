from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Polis, num_check, service_check, request_to_sk, request_to_service_db, num_to_regex
from .serializers import PolisSerializer, NotFoundPolisSerializer
from urllib.parse import unquote_plus
import json, re


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
        #company = request.data['company']
        #polis_number = request.data['polis_number']
        #polis_type = request.data['polis_type']
        #services = request.data['services']
        
        serializer = PolisSerializer(request.data)
        if serializer.is_valid():     
            try:
                polis = numcheck(request.data['polis_number'])[-1]
            except ObjectDoesNotExist:
                regex = num_to_regex(request.data['polis_number'])
                nf_serializer = NotFoundPolisSerializer(company_name=request.data['company'], 
                                                        num_regex=regex, 
                                                        polis_type=request.data['polis_type'])
                if nf_serializer.is_valid():
                    polis = nf_serializer.save()
                else:
                    return Response(nf_serializer.errors)
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
                resp = request_to_sk(serializer.validated_data)
                polis.BILLING += 1
                polis.save()
                return Response(resp)
            except ObjectDoesNotExist:
                polis.not_found_search += 1
                polis.save()
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
