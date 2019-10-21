from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Polis
from .serializers import PolisSerializer


class PolisView(APIView):
    def get(self, request):
        polises = Polis.objects.all()
        serializer = PolisSerializer(polises, many=True)
        return Response({'polises': serializer.data})
