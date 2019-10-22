from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Polis, num_check, service_check, request_to_sk, request_to_service_db
import json

class SearchView(APIView):
    def get(self, request):
        number = request.GET.get('number', None)
        service = request.GET.get('service', None)
      
        if number:
            resp = {}
            try:
                resp['company'], resp['polis_type'] = num_check(number)
                return Response(resp)
            except ObjectDoesNotExist:
                return Response(resp)
        
        if service:
            in_database = service_check(service)
            return Response({'service_in_base': in_database})        


class PolisCheckView(APIView):
    def get(self, request):
        company = request.GET.get('company')
        polis_type = request.GET.get('type')
        number = request.GET.get('number')
        services = request.GET.get('services').split('+')
      
        try:
            (
                polis_ltd_sk, 
                polis_ltd_type, 
                polis_ltd_id, 
                polis_ltd_date_end, 
                polis_ltd_tel,
            ) = request_to_sk(company, number, polis_type)
        except ObjectDoesNotExist:
            raise Http404 
        
        (
            polis_ltd_inservice,
            polis_ltd_notservice,
            polis_ltd_notfoundservice,
        ) = request_to_service_db(services)
        
        return Response(json.dumps(
            {
                 'polis_ltd_sk': polis_ltd_sk, 
                 'polis_ltd_type': polis_ltd_type, 
                 'polis_ltd_id': polis_ltd_id, 
                 'polis_ltd_date_end': polis_ltd_date_end, 
                 'polis_ltd_tel': polis_ltd_tel,
                 'polis_ltd_inservice': polis_ltd_inservice,
                 'polis_ltd_notservice': polis_ltd_notservice,
                 'polis_ltd_notfoundservice': polis_ltd_notfoundservice,
            }, indent=4)
        )
