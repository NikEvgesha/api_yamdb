from django.db import models


class NameAndSlug(models.Model):
    name = models.CharField('Заголовок', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True,
                            max_length=50)

    class Meta:
        abstract = True


class Category(NameAndSlug):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:30]


class Genre(NameAndSlug):
    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание')
    year = models.IntegerField('Год публикации')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр публикации',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    @property
    def rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        return sum(reviews.score for reviews in reviews) / reviews.count()
