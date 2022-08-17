from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework import routers
from users.views import ConfirmTokenView, RegisterView, UserViewSet

router_v1 = routers.DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/'
                   r'reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', RegisterView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/', ConfirmTokenView.as_view(), name='token_refresh'),
]
