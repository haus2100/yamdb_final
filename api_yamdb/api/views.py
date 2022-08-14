from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .filters import GenreFilter, TitleFilter
from .mixins import CreateListDeleteMixinSet
from .permissions import (AdminOrSuperuser, IsAdminModeratorOwnerOrReadOnly,
                          IsAuthenticatedOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class CategoryViewSet(CreateListDeleteMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('=name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create':
            return (AdminOrSuperuser(),)
        if self.action == 'destroy':
            return (AdminOrSuperuser(),)
        return super().get_permissions()


class GenreViewSet(CreateListDeleteMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    filter_class = GenreFilter

    def get_permissions(self):
        if self.action == 'create':
            return (AdminOrSuperuser(),)
        if self.action == 'destroy':
            return (AdminOrSuperuser(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = (
        'category__slug',
        'genre__slug',
        'name',
        'year')

    def get_serializer_class(self):
        if self.action in (
            'list',
            'retrieve'
        ):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_permissions(self):
        if self.action in (
            'create',
            'destroy',
            'partial_update'
        ):
            return (AdminOrSuperuser(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(rating=None)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
