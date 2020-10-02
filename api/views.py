from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .filters import TitleFilter
from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleListSerializer, TitlePostSerializer
)
from .permissions import ReadOnly


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
