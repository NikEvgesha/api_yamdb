from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from api.serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserTokenSerializer,
    UserMeSerializer
)
from api.permissions import IsAdminOrSuperuser
from users.pagination import UserPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = UserPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False,
            permission_classes=[IsAuthenticated, ],
            methods=['GET', 'PATCH'])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Неверные данные', status=status.HTTP_400_BAD_REQUEST)


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        user = User.objects.filter(username=username, email=email)
        if user.exists():
            token = default_token_generator.make_token(user[0])
            send_confirmation_code(user[0], token)
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_duplicates = User.objects.filter(
            Q(username=username)
            | Q(email=email)
        )
        if user_duplicates.exists():
            return Response(
                'Имя пользователя или е-мейл уже используются',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        token = default_token_generator.make_token(user[0])
        send_confirmation_code(user[0], token)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetToken(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def post(self, request):
        username = request.data.get('username')
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=username)
        if user.exists():
            serializer = UserTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(get_token(user[0]), status=status.HTTP_201_CREATED)
        return Response('Некорректные данные',
                        status=status.HTTP_404_NOT_FOUND)


def send_confirmation_code(user, confirmation_code):
    send_mail(
        'YaMDB: Ваш код подтверждения',
        f'Код подтверждения: {confirmation_code}',
        'yamdb@yamdb.fake',
        [user.email, ],
        fail_silently=False
    )


def get_token(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token)
    }
