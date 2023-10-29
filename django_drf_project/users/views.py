from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from lesson_manage import permissions
from .serializers import MyTokenObtainPairSerializer, UserSerializer


# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Ваш код представления
    return Response({'message': 'Авторизовано!'})
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Ваша кастомная логика сохранения пользователя
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


