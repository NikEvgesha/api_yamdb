from rest_framework import serializers

from .models import Review, Comment


class ReviewSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date'],


class CommentSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'review', 'author', 'text', 'pub_date']
