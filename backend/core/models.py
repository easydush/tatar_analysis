from django.db import models
from django.utils.translation import gettext_lazy as _

MAX_LENGTH = 255
VK_URL = 'https://vk.com'


class Source(models.TextChoices):
    VK = 'VK', _('VK')
    ELIBRARY = 'ELIBRARY', _('ELIBRARY')
    KPFU = 'KPFU', _('KPFU')


class Article(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=MAX_LENGTH)
    source = models.CharField(max_length=8, choices=Source.choices, blank=False)
    link = models.URLField()
    file = models.FileField(upload_to='articles/')
    text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.source} | {self.title}'

    class Meta:
        ordering = ('author',)
