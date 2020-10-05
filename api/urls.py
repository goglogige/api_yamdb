from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CommentViewSet, ReviewViewSet
from .views import TitleViewSet, CategoryDestroy, CategoryListCreate, GenreListCreate, GenreDestroy
from .views import (
    confirm_email,
    registration,
    GetPatchYourProfile,
    UsersViewSet,
)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
# router.register('titles', TitleViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/email/', confirm_email),
    path('v1/auth/token/', registration),
    path('v1/users/me/', GetPatchYourProfile.as_view()),
    path('v1/api-token-auth/', obtain_auth_token),
    # path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/categories/', CategoryListCreate.as_view()),
    path('v1/categories/<str:slug>/', CategoryDestroy.as_view()),
    path('v1/genres/', GenreListCreate.as_view()),
    path('v1/genres/<str:slug>/', GenreDestroy.as_view()),
    path('v1/', include(router.urls)),

]


