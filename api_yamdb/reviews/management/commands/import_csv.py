import csv
import os

from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Review, Comment, Title, Category, Genre
from api_yamdb.settings import BASE_DIR


def user_import(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def category_import(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_import(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def title_import(row):
    category_obj = Category.objects.get(id=row[3])
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category=category_obj
    )


def genre_title_import(row):
    title_obj = Title.objects.get(id=row[1])
    genres_obj = Genre.objects.get(id=row[2])
    title_obj.genre.add(genres_obj)


def review_import(row):
    title_obj = Title.objects.get(id=row[1])
    author_obj = User.objects.get(id=row[3])
    Review.objects.get_or_create(
        id=row[0],
        title_id=title_obj.id,
        text=row[2],
        author=author_obj,
        score=row[4],
        pub_date=row[5]
    )


def comment_import(row):
    review_obj = Review.objects.get(id=row[1])
    author_obj = User.objects.get(id=row[3])
    Comment.objects.get_or_create(
        id=row[0],
        review_id=review_obj.id,
        text=row[2],
        author=author_obj,
        pub_date=row[4]
    )


import_functions = {
    'users.csv': user_import,
    'category.csv': category_import,
    'genre.csv': genre_import,
    'titles.csv': title_import,
    'genre_title.csv': genre_title_import,
    'review.csv': review_import,
    'comments.csv': comment_import,
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for filename, func in import_functions.items():
            filepath = os.path.join(BASE_DIR, "static/data/") + filename
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    func(row)
