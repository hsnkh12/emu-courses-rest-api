from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .serializers import CourseSerializer, ResourceSerializer
from .models import Course, Resource, Like


class CoursesController(ViewSet):

    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['code','name','department__name']
    search_fields = ['name__startswith','code__startswith']

    def list(self, request):

       queryset = self.get_queryset()
       serializer = CourseSerializer(queryset, fields=['code','name'] ,many=True)

       return Response(serializer.data)

    def retrieve(self, request, pk=None):

        queryset = self.get_queryset().get(code=pk)
        serializer = CourseSerializer(queryset)

        return Response(serializer.data)

    def get_queryset(self):
        return Course.objects.select_related('department')


class ResourcesController(ViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course__code','title']

    def list(self, request):
        pass

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass