from django.db.models import Avg
from django.shortcuts import get_object_or_404
from reviews.models import Title


def update_rating(title_id):
    title = get_object_or_404(Title, id=title_id)
    reviews = title.reviews.all()
    title.rating = reviews.all().aggregate(Avg('score'))['score__avg']
    title.save()
