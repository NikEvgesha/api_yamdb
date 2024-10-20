import csv
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from users.models import User
from titles.models import Title, Category, Genre
from reviews.models import Review, Comment


with open('static/data/users.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        obj = User.objects.get_or_create(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[3],
            bio=row[4],
            first_name=row[5],
            last_name=row[6],
        )

with open('static/data/category.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:

        obj = Category.objects.get_or_create(
            id=row[0],
            name=row[1],
            slug=row[2],
        )

with open('static/data/genre.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:

        obj = Genre.objects.get_or_create(
            id=row[0],
            name=row[1],
            slug=row[2],
        )


with open('static/data/titles.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        category_obj = Category.objects.get(id=row[3])
        obj = Title.objects.get_or_create(
            id=row[0],
            name=row[1],
            year=row[2],
            category=category_obj
        )

with open('static/data/genre_title.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        title_obj = Title.objects.get(id=row[1])
        genres_obj = Genre.objects.get(id=row[2])
        title_obj.genre.add(genres_obj)
        

with open('static/data/review.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        title_obj = Title.objects.get(id=row[1])
        author_obj = User.objects.get(id=row[3])
        obj = Review.objects.get_or_create(
            id=row[0],
            title_id=title_obj.id,
            text=row[2],
            author=author_obj,
            score=row[4],
            pub_date=row[5]
        )

with open('static/data/comments.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        review_obj = Review.objects.get(id=row[1])
        author_obj = User.objects.get(id=row[3])
        obj = Comment.objects.get_or_create(
            id=row[0],
            review_id=review_obj.id,
            text=row[2],
            author=author_obj,
            pub_date=row[4]
        )
