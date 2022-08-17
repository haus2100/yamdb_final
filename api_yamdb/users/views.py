from api.permissions import IsAdminOrOwner
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import (RegisterSerializer, UserLoginSerializer,
                               UserSerializer)
from users.utils import Utils

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение пользователя по username (GET).
    Добавление пользователя (POST).
    Изменение данных пользователя по username (PATCH).
    Удаление пользователя по username (DELETE).
    Права доступа: Администратор
    Поля email и username для POST и PATCH запросов должны быть уникальными.
    """

    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrOwner,)
    serializer_class = UserSerializer

    @action(methods=['patch', 'get'], detail=False)
    def me(self, request):
        """
        Получение данных своей учетной записи (GET).
        Изменение данных своей учетной записи (PATCH).
        Права доступа: Любой авторизованный пользователь
        Поля email и username для PATCH запроса должны быть уникальными.
        """
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

            if (user.is_user
                    and serializer.validated_data.pop(
                        'role', 'user')
                    != user.role):
                return Response(
                    serializer.data,
                    status=status.HTTP_403_FORBIDDEN)

            self.perform_update(serializer)
            return Response(serializer.data)
        return False


class RegisterView(generics.CreateAPIView):
    """
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Поля email и username должны быть уникальными.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = Utils.token_generator.make_token(user)

        email_body = (
            f'Добрый день, {user.username}! '
            f'Ваш confirmation_code: {token}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Ваш Токен YamDB!'
        }
        Utils.send_email(data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers)


class ConfirmTokenView(generics.RetrieveAPIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if (user is not None
                and Utils.token_generator.check_token(
                    user, confirmation_code)):

            user.is_active = True
            user.save()
        else:
            response = {
                'confirmation_code': 'Токен не валидный'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user)
        response = {
            'token': str(token.access_token)
        }
        return Response(response, status=status.HTTP_200_OK)
