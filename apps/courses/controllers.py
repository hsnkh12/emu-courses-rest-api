from tokenize import _all_string_prefixes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CourseSerializer, LikeSerializer, ResourceSerializer, RateSerializer
from .models import Course, Rate, Resource, Like
from ..utils.serializers import ValidationCheck
from .permessions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status



class CourseListController(ListAPIView):

    queryset = Course.objects
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['code','name','department__name']
    search_fields = ['^name','^code','=name','=code']
    ordering_fields = ['name','code','credit']

    def get_serializer(self, *args, **kwargs):

        serializer_class = CourseSerializer
        kwargs.setdefault('fields',['code','name','difficulty_rate'])
        return serializer_class(*args, **kwargs)


class CourseRetrieveController(APIView):

    def get(self, request, pk=None):

        object = self.get_queryset().get(code=pk)
        serializer = CourseSerializer(object)

        return Response(serializer.data)

    def get_queryset(self):
        return Course.objects.select_related('department')


class ResourceListController(ListAPIView):

    queryset = Resource.objects.select_related('user')
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = ['course__code','title']
    ordering_fields = ['likes_count']
    

class ResourceRetrieveController(ViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]


    def retrieve(self, request, pk=None):

        object = self.get_queryset().get(pk = pk)
        serializer = ResourceSerializer(object)

        return Response(serializer.data)

    def create(self, request):

        course_code = request.query_params.get('course__code')

        try:
            course = Course.objects.get(code=course_code)
        except:
            return Response({"course__code":["This query parameter is required."]})

        serializer = ResourceSerializer(data= request.data, fields= ['title', 'url', 'description', 'date_added'])
        return ValidationCheck(serializer, user=request.user, course = course)

    def update(self, request, pk=None):
        
        object = self.get_queryset().get(pk = pk)
        serializer = ResourceSerializer(object, fields= ['title', 'url', 'description'] ,data=request.data)

        return ValidationCheck(serializer)
        
    def get_queryset(self):
        return Resource.objects.select_related('user')



class LikeController(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        
        resource = Resource.objects.get(pk=pk)

        if not self.get_queryset().filter(resource__id = pk).exists():
            serializer = LikeSerializer(data = request.data)
            return ValidationCheck(serializer, user=request.user, resource=resource)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk=None):

        like_object = self.get_queryset().get(resource__id = pk)
        like_object.delete()
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        return Like.objects



class RateController(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):

        course = Course.objects.get(code= pk)

        if not request.user.rates_related.filter(course = course).exists():

            serializer = RateSerializer(data = request.data)
            return ValidationCheck(serializer, user=request.user, course=course)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        