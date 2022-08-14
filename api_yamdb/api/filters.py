import django_filters
from reviews.models import GenreTitle, Title


class GenreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        name='genre__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = GenreTitle
        fields = ['genre']


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug',)
    category = django_filters.CharFilter(field_name='category__slug',)
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ['year']
