from rest_framework.authtoken import views
from .controllers import SignupController, SignoutController, ProfileController, ReportResourceController
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    
    path('signin/', obtain_auth_token, name='signin'),
    path('signup/', SignupController, name='signup'),
    path('profile/', ProfileController, name='profile'),
    path('signout/', SignoutController, name='signout'),
    path('report-resource/<pk>/', ReportResourceController, name='report-resource')
]