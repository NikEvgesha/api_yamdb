from rest_framework import viewsets, views, status

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationAPIView(views.APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access

            refresh.payload.update({    # Полезная информация в самом токене

                'user_id': user.id,

                'username': user.username

            })

            return Response({

                'refresh': str(refresh),

                'access': str(refresh.access_token),  # Отправка на клиент

            }, status=status.HTTP_201_CREATED)
