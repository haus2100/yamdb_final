from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

FORBIDDEN_NAME = 'Username с таким наименованием уже зарегистрирован'
FORBIDDEN_EMAIL = 'Пользователь с таким email уже зарегистрирован'
MISSING_USERNAME = 'Для аутентификации требуется ввести имя пользователя'
MISSING_CODE = 'Для аутентификации требуется ввести код подтверждения'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if (User.objects.filter(username=value).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                FORBIDDEN_NAME
            )
        return value

    def validate_email(self, value):
        if (User.objects.filter(email=value).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                FORBIDDEN_EMAIL
            )
        return value

    class Meta:
        fields = (
            "username", "email", "first_name",
            "last_name", "bio", "role",
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'))
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
    )

    def validate(self, value):
        if value['username'] == 'me':
            raise serializers.ValidationError(
                {"username": "Имя пользователя не может быть 'me'"})

        user_by_email = User.objects.filter(
            email=value['email']).exists()
        user_by_username = User.objects.filter(
            username=value['username']).exists()

        if user_by_email:
            raise serializers.ValidationError(
                {"email": f"Адрес '{value['email']}' уже занят"})
        if user_by_username:
            raise serializers.ValidationError(
                {"username": f"Юзернейм '{value['username']}' уже занят"})

        return value

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
            defaults={'is_active': False},
        )

        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(MISSING_USERNAME)
        if confirmation_code is None:
            raise serializers.ValidationError(MISSING_CODE)
        return data
