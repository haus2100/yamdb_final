from django.db import models
from reviews.validators import validate_score, validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('id',)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('id',)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='TitleGenre',
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        db_index=True
    )
    rating = models.PositiveIntegerField(
        validators=(validate_score,),
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        db_index=True
    )
    text = models.CharField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.PositiveIntegerField(validators=(validate_score,))
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            )
        ]
        ordering = ('id',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE, null=True,
        related_name='comments',
        db_index=True
    )
    text = models.CharField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('id',)


class TitleGenre(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ('id',)
