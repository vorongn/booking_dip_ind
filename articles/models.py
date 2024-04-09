from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    content = models.TextField(verbose_name='содержание')
    status = models.BooleanField(default=False, verbose_name='опубликовать')
    homepage_status = models.BooleanField(default=False, verbose_name='на главной странице')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


