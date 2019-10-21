from django.shortcuts import render

class PolisView(APIView):
    def get(self, request):
        polises = Polis.objects.all()
        serializer = PolisSerializer(polises, many=True)
        return Response({'polises': serializer.data})
