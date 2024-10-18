from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
# from rest_framework.decorators import action
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserTokenSerializer
)
from users.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsAdmin]


class RetrieveUpdateViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        confirmation_code = '1234'

        user = User.objects.filter(username=username, email=email)
        if user.exists():
            user = user[0]
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(user)
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        else:
            user_duplicates = User.objects.filter(
                Q(username=username)
                | Q(email=email)
            )
            if user_duplicates.exists():
                return Response(
                    'Неверные данные',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = get_object_or_404(User, username=username)
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetToken(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(get_token(user), status=status.HTTP_201_CREATED)


def send_confirmation_code(user):
    send_mail(
        'YaMDB: Ваш код подтверждения',
        f'Код подтверждения: {user.confirmation_code}',
        'yamdb@yamdb.fake',
        [user.email,],
        fail_silently=False
    )


def token():
    ...


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
