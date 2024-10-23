from django.shortcuts import get_object_or_404
from rest_framework import exceptions, pagination, viewsets

from .models import Review
from .permissions import IsAdminModeratorAuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получение отзывов
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
    
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed(method='PUT')
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        review = self.get_post()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_post()
        serializer.save(author=self.request.user, review=review)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed(method='PUT')
        return super().update(request, *args, **kwargs)