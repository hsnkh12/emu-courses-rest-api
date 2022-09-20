from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .controllers import (CourseListController, 
CourseRetrieveController, 
ResourceListController, 
ResourceRetrieveController,
LikeController,
RateController
)

router = DefaultRouter()

router.register('resources', ResourceRetrieveController, basename='resources')

urlpatterns = [

    path('courses/', include([
        path('',CourseListController.as_view(),name='courses'),
        path('<pk>/',CourseRetrieveController.as_view(),name='course-detail'),
        path('<pk>/rate/',RateController.as_view(),name='rate')
    ])),
    
    path('resources/', include([
        path('',ResourceListController.as_view(),name='resources-detail'),
        path('<pk>/like',LikeController.as_view(), name='like'),
    ]))
    
    
] + router.urls