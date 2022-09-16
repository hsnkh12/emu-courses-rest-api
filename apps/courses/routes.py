from rest_framework.routers import DefaultRouter
from django.urls import path
from .controllers import (CourseListController, 
CourseRetrieveController, 
ResourceListController, 
ResourceRetrieveController,
LikeController
)

router = DefaultRouter()

router.register('resources', ResourceRetrieveController, basename='resources')

urlpatterns = [

    path('courses/',CourseListController.as_view(),name='courses'),
    path('courses/<pk>/',CourseRetrieveController.as_view(),name='course-detail'),
    path('resources/',ResourceListController.as_view(),name='resources-detail'),
    path('resources/<pk>/like',LikeController.as_view(), name='like')
] + router.urls