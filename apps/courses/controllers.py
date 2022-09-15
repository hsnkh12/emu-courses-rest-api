from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend




class CoursesController(ViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

class ResourcesController(ViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course__id']

    def list(self, request):
        pass

    def create(self, request):
        pass