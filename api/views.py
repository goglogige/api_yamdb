from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, serializers
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .code import CODE
from .filters import TitleFilter
from .models import Category, Genre, Title
from .models import Review
from .models import User
from .permissions import IsAdministrator
from .permissions import IsAuthorOrIsStaffPermission
from .permissions import ReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleListSerializer, TitlePostSerializer
)
from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer
from .serializers import UserSerializer, EmailSerializer, UserCreateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def confirm_email(request):
    serializer = EmailSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data['email']
    send_mail(
        'Confirmation code',
        f'You confirmation code: {CODE}.',
        'evg.katolichenko@gmail.com',
        [email],
        fail_silently=False,
    )
    return Response({'message': f'Confirmation code ****** sent to {email}'})


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    email = serializer.data['email']
    confirmation_code = serializer.data['confirmation_code']
    if confirmation_code != str(CODE):
        raise serializers.ValidationError(
            {"confirmation_code": "Confirmation code does not match."})
    if User.objects.filter(email=email).count() == 0:
        user = User.objects.create(email=email)
    else:
        user = User.objects.get(email=email)
    token = RefreshToken.for_user(user)
    user_exist = User.objects.filter(email=email).count()
    return Response({
        'token': f'{token.access_token}',
        'user': f'{user}',
        'user_exist': f'{user_exist}',
    },
        status=status.HTTP_200_OK)


class GetPatchYourProfile(APIView):
    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]
    lookup_field = 'username'

    @action(detail=True, methods=['GET', 'POST'])
    def get_create_users(self, request):
        users_list = User.objects.all()
        serializer = UserSerializer(users_list, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'PATCH', 'DELETE'])
    def actions_users(self, request):
        user = get_object_or_404(User, username=self.request.data['username'])
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    lookup_field = "slug"


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitlePostSerializer

    # serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrIsStaffPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')
        )

    def partial_update(self, request, *args, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        get_object_or_404(
            title.reviews,
            pk=self.kwargs.get('pk'),
            title_id=self.kwargs.get('title_id')
        )
        return super().partial_update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsStaffPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        get_object_or_404(
            title.reviews,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id')
        )

    def partial_update(self, request, *args, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        review = get_object_or_404(
            title.reviews,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        get_object_or_404(
            review.comments,
            pk=self.kwargs.get('pk'),
            review_id=self.kwargs.get('review_id')
        )
        return super().partial_update(request, *args, **kwargs)

