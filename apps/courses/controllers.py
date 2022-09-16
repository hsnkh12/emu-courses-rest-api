from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CourseSerializer, ResourceSerializer
from .models import Course, Department, Resource, Like
from ..utils.serializers import ValidationCheck
from .permessions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView




class CourseListController(ListAPIView):

    queryset = Course.objects
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['code','name','department__name']
    search_fields = ['^name','^code','=name','=code']
    ordering_fields = ['name','code','credit']

    def get_serializer(self, *args, **kwargs):

        serializer_class = CourseSerializer
        kwargs.setdefault('fields',['code','name'])
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
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['course__code','title']
    



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



#Like cotroller
#Rate comtroller