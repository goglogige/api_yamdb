from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryDestroy, CategoryListCreate, GenreListCreate, GenreDestroy
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/api-token-auth/', obtain_auth_token),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/categories/', CategoryListCreate.as_view()),
    path('v1/categories/<str:slug>/', CategoryDestroy.as_view()),
    path('v1/genres/', GenreListCreate.as_view()),
    path('v1/genres/<str:slug>/', GenreDestroy.as_view()),
    path('v1/', include(router.urls)),
]
