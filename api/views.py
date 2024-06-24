import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Starship
from .serializers import StarshipSerializer

class StarshipPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

class StarshipView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StarshipPagination

    def get(self, request, pk=0):
        if pk == 0:
            starships = Starship.objects.all()
            paginator = StarshipPagination()
            paginated_starships = paginator.paginate_queryset(starships, request)
            starship_serializer = StarshipSerializer(paginated_starships, many=True)
            return paginator.get_paginated_response(starship_serializer.data)
        else:
            starship = Starship.objects.filter(id=pk).first()
            if starship:
                starship_serializer = StarshipSerializer(starship)
                return JsonResponse({'starship': starship_serializer.data}, status=200)
            return JsonResponse({'error': 'Starship not found'}, status=404)

    def post(self, request):
        rq = json.loads(request.body)
        starship_serializer = StarshipSerializer(data=rq)
        if starship_serializer.is_valid():
            starship_serializer.save()
            return JsonResponse({'starship': starship_serializer.data}, status=201)
        return JsonResponse(starship_serializer.errors, status=400)

    def put(self, request, pk):
        rq = json.loads(request.body)
        starship = Starship.objects.get(id=pk)
        starship_serializer = StarshipSerializer(starship, data=rq, partial=True)
        if starship_serializer.is_valid():
            starship_serializer.save()
            return JsonResponse({'starship': starship_serializer.data}, status=200)
        return JsonResponse(starship_serializer.errors, status=400)

    def delete(self, request, pk):
        starship = Starship.objects.get(id=pk)
        starship.delete()
        return JsonResponse({}, status=204)

class StarshipSearchView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name):
        starships = list(Starship.objects.values().filter(name__contains=name))
        return JsonResponse({'starships': starships}, status=200)

class StarshipViewXML(View):
    def get(self, request):
        data = serializers.serialize('xml', Starship.objects.all())
        return HttpResponse(data, content_type='application/xml')
    
class StarshipViewSet(viewsets.ModelViewSet):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


# ejemplo manual sin serializadores
# class StarshipView(View):
#     @method_decorator(login_required)
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super(StarshipView, self).dispatch(*args, **kwargs)

#     def get(self, request, pk=0):
#         if pk == 0:
#             starships = list(Starship.objects.values())
#             return JsonResponse({'starships': starships}, status=200)
#         else:
#             starship = list(Starship.objects.values().filter(id=pk))
#             return JsonResponse({'starship': starship}, status=200)
    
#     def post(self, request):
#         rq = json.loads(request.body)
#         starship = Starship(name=rq['name'], model=rq['model'], passengers=rq['passengers'], cargo_capacity=rq['cargo_capacity'])
#         starship.save()
#         return JsonResponse({'starship': starship.id}, status=201)
    
#     def put(self, request, pk):
#         rq = json.loads(request.body)
#         starship = Starship.objects.get(id=pk)
#         if 'name' in rq:
#             starship.name = rq['name']
#         if 'model' in rq:
#             starship.model = rq['model']
#         if 'passengers' in rq:
#             starship.passengers = rq['passengers']
#         if 'cargo_capacity' in rq:
#             starship.cargo_capacity = rq['cargo_capacity']
#         starship.save()
#         return JsonResponse({'starship': starship.id}, status=200)
    
#     def delete(self, request, pk):
#         starship = Starship.objects.get(id=pk)
#         starship.delete()
#         return JsonResponse({}, status=204)
    
# class StarshipSearchView(View):
#     def get(self, request, name):
#         starships = list(Starship.objects.values().filter(name__contains=name))
#         return JsonResponse({'starships': starships}, status=200)