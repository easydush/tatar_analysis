from django.db import models
from django.db.models import Manager

MAX_LENGTH = 255


class Article(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=MAX_LENGTH)
    article_link = models.URLField()
    file = models.CharField(max_length=MAX_LENGTH)
    text = models.TextField(blank=True)
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} [{self.rate}] - [{self.article_link}]'

    class Meta:
        ordering = ('author',)


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
