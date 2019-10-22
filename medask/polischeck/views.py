from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Polis, num_check, service_check
from .serializers import PolisSerializer


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


class PolisView(APIView):
    def get(self, request):
        polises = Polis.objects.all()
        serializer = PolisSerializer(polises, many=True)
        return Response({'polises': serializer.data})
