import hashlib
from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status, mixins, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from api.serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserTokenSerializer,
    UserMeSerializer
)
from api.permissions import IsAdmin, IsSuperuser
from users.pagination import UserPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperuser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = UserPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(url_path='me',
            detail=False,
            permission_classes=[IsAuthenticated, ],
            methods=['GET', 'PATCH'])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == "GET":
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Неверные данные', status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveUpdateViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    pass


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        user = User.objects.filter(username=username, email=email)
        if user.exists():
            user = user[0]
            confirmation_code = generate_confirmation_code(username)
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(user)
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        else:
            serializer = UserSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_duplicates = User.objects.filter(
                Q(username=username)
                | Q(email=email)
            )
            if user_duplicates.exists():
                return Response(
                    'Неверные данные',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            user = get_object_or_404(User, username=username)
            confirmation_code = generate_confirmation_code(username)
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
        confirmation_code = request.data.get('confirmation_code')
        if not username or not confirmation_code:
            return Response(
                'Поля username и confirmation_code являются обязательными!',
                status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=username)
        if user.exists():
            serializer = UserTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(get_token(user[0]), status=status.HTTP_201_CREATED)
        return Response('Некорректные данные',
                        status=status.HTTP_404_NOT_FOUND)


def generate_confirmation_code(username):
    timestamp = datetime.now().timestamp()
    fields = (username, str(timestamp))
    data = ''.join(fields).encode('utf-8')
    code = hashlib.sha256(data).hexdigest()
    return code


def send_confirmation_code(user):
    send_mail(
        'YaMDB: Ваш код подтверждения',
        f'Код подтверждения: {user.confirmation_code}',
        'yamdb@yamdb.fake',
        [user.email, ],
        fail_silently=False
    )


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
