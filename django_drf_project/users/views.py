from django.shortcuts import render

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MyTokenObtainPairSerializer

# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Ваш код представления
    return Response({'message': 'Авторизовано!'})
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


