from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='rewievs',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва')
    # Временно используем IntegerField для хранения ID пользователя
    # пока не импортирована модель User
    author = models.IntegerField('ID пользователя')
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.title} - {self.score} баллов'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    # Временно используем IntegerField для хранения ID пользователя
    # пока не импортирована модель User
    author = models.IntegerField('ID пользователя')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к {self.review}'
