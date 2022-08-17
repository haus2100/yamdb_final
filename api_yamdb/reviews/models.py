from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        'Наименование категории',
        max_length=256
    )
    slug = models.SlugField(
        'Адрес категории',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        'Наименование жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Адрес жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='category',
        blank=True,
        null=False,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    name = models.CharField(
        'Название произведения',
        max_length=256,
        blank=False
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        db_index=True,
        validators=(validate_year,),
    )
    rating = models.IntegerField(
        'Рейтинг поста',
        null=True
    )
    description = models.TextField(
        'Описание произведения',
        blank=True
    )

    class Meta:
        ordering = ('year', )
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Произведение {self.name}, рейтинг {self.rating}'


class GenreTitle(models.Model):
    """Связанная таблица жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='genre',
        blank=True,
        null=False,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('genre', )
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Отзывы пользователей"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Выберите значения от 1 до 10'),
            MaxValueValidator(10, 'Выберите значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Комментарии"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
