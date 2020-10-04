from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    confirm_email,
    registration,
    GetPatchYourProfile,
    UsersViewSet,
)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/email/', confirm_email),
    path('v1/auth/token/', registration),
    path('v1/users/me/', GetPatchYourProfile.as_view()),
    path('v1/', include(router.urls)),
]
