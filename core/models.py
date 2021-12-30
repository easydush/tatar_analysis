from datetime import datetime

from django.db import models
from django.db.models import Manager

MAX_LENGTH = 255


class UncheckedYandexNewsItem(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(checked=False)


class YandexNewsTopic(models.Model):
    name = models.CharField(max_length=500, db_index=True)
    rss_url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - [{self.rss_url}]'

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'rss_url')


class YandexNewsItem(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(max_length=350, unique=True)
    pub_date = models.DateTimeField()
    hash = models.CharField(max_length=100, unique=True)
    checked = models.BooleanField(default=False)

    objects = Manager()
    unchecked = UncheckedYandexNewsItem()

    def __str__(self):
        return f'{self.title} [{self.pub_date}] [{self.checked}] [{self.hash}] [{self.link}]'


class TriggerPhrase(models.Model):
    name = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class TriggerNews(models.Model):
    YANDEX = 0
    VK = 1
    NEWS_TYPE_CHOICES = (
        (YANDEX, 0),
        (VK, 1)
    )
    POSITIVE = 0
    NEGATIVE = 1
    SKIP = 2
    NEUTRAL = 3
    UNKNOWN = 4
    TONE_TYPE_CHOICES = (
        (POSITIVE, 0),
        (NEGATIVE, 1),
        (SKIP, 2),
        (NEUTRAL, 3),
        (UNKNOWN, 4),
    )
    title = models.CharField(max_length=300)
    article_link = models.URLField()
    last_update = models.DateTimeField(default=datetime.now)
    description = models.TextField(blank=True)
    rate = models.PositiveIntegerField(default=0)
    trigger_word = models.ManyToManyField(TriggerPhrase)
    news_type = models.IntegerField(choices=NEWS_TYPE_CHOICES, default=YANDEX)
    tone_type = models.SmallIntegerField(choices=TONE_TYPE_CHOICES, default=NEUTRAL)
    tone_value = models.FloatField(default=1.0)

    def __str__(self):
        return f'{self.title} [{self.rate}] [type - {self.news_type}]- [{self.article_link}]'

    class Meta:
        ordering = ('-last_update', '-rate')
        verbose_name = 'Trigger news'
        verbose_name_plural = 'Trigger news'


class UncheckedVKPost(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(checked=False)


class VKSource(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    vk_id = models.CharField(max_length=32, primary_key=True, unique=True)

    def __str__(self):
        return f'{self.name} - [{self.vk_id}]'

    class Meta:
        ordering = ('name',)


class VKGroup(models.Model):
    vk_id = models.IntegerField(null=True, unique=True)
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField(blank=True, null=True)
    members_count = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)
    site = models.CharField(max_length=MAX_LENGTH, null=True)
    photo_100 = models.CharField(max_length=MAX_LENGTH)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - [{self.vk_id}]'

    def link(self):
        return f'https://vk.com/public{self.vk_id}'

    class Meta:
        ordering = ('name',)


class VKPost(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    owner = models.ForeignKey(VKGroup, on_delete=models.CASCADE)
    address = models.SlugField(
        max_length=MAX_LENGTH,
        null=False,
        blank=False,
        unique=True
    )
    pub_date = models.DateField()
    text = models.TextField(blank=True, null=True)
    comments = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()
    reposts = models.PositiveSmallIntegerField()
    checked = models.BooleanField(default=False)
    objects = Manager()
    unchecked = UncheckedVKPost()

    def save(self, *args, **kwargs):
        self.address = f'https://vk.com/wall-{self.owner.vk_id}_{self.id}'
        super(VKPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-pub_date',)
