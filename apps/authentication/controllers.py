from rest_framework.response import Response
from .serializers import RegistrationSerializer, ProfileSerializer, ReportSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..utils.serializers import ValidationCheck

@api_view(['POST'])
def SignupController(request):

    serializer = RegistrationSerializer(data = request.data)

    if serializer.is_valid():

        new_user  = serializer.save()
        token = Token.objects.get(user=new_user).key

        data = {
            "Token":token
        }
        return Response(data)
    
    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfileController(request):
    
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def SignoutController(request):

    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def ReportResourceController(request, pk=None):
    
    from ..courses.models import Resource
    resource = Resource.objects.get(pk=pk)
    serializer = ReportSerializer(data = request.data)
    return ValidationCheck(serializer, resource = resource)