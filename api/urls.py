from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import CommentViewSet, ReviewViewSet, TitleViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]