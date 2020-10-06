from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (CategoryDestroy, CategoryListCreate, CommentViewSet,
                    GenreDestroy, GenreListCreate, GetPatchYourProfile,
                    ReviewViewSet, TitleViewSet, UsersViewSet, confirm_email,
                    registration)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/email/', confirm_email),
    path('v1/auth/token/', registration),
    path('v1/users/me/', GetPatchYourProfile.as_view()),
    path('v1/api-token-auth/', obtain_auth_token),
    path('v1/categories/', CategoryListCreate.as_view()),
    path('v1/categories/<str:slug>/', CategoryDestroy.as_view()),
    path('v1/genres/', GenreListCreate.as_view()),
    path('v1/genres/<str:slug>/', GenreDestroy.as_view()),
    path('v1/', include(router.urls)),

]


