from rest_framework import serializers
from django.shortcuts import get_object_or_404
# from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'confirmation_code',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role']
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другое имя пользователя!')
        return data


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role']


class UserSignupSerializer(serializers.ModelSerializer):
    # username = serializers.SlugField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())])
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):

        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другое имя пользователя!')
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError(
                'Неверный код подтверждения')
        return data
