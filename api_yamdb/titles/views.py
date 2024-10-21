from rest_framework import viewsets
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from rest_framework.response import Response
from rest_framework import status
from titles.permissions import IsAdminOrSuperUser
from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend


class CategoryAndGenreClass(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        """Обрабатываем DELETE-запрос для удаления категории."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """Запрещаем GET-запросы для конкретного URL."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """Запрещаем PATCH-запросы для конкретного URL."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(CategoryAndGenreClass):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreClass):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrSuperUser,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('category__slug', 'genre__slug', 'year', 'name')

    def get_queryset(self):
        "Для фильтрации"
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre', None)
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name=name)
        return queryset

    def format_data(self, data):
        for item in data:
            category_instance = Category.objects.get(slug=item['category'])
            item['category'] = {
                'name': category_instance.name,
                'slug': category_instance.slug
            }
            item['genre'] = [
                {'name': genre.name, 'slug': genre.slug}
                for genre in Genre.objects.filter(slug__in=item['genre'])
            ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            self.format_data(data)
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data 
        self.format_data(data)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.format_data([data])
        return Response(data)
