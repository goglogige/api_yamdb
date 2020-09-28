from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer

from .models import Review, Title
from .permissions import IsAuthorOrIsStaffPermission


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination


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
