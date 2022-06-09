from django.db import models

MAX_LENGTH = 255
VK_URL = 'https://vk.com'


# VK models
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
        return f'{VK_URL}/public{self.vk_id}'

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
    text = models.TextField(blank=True, null=True)

    def save_as_vk_post(self, *args, **kwargs):
        self.address = f'{VK_URL}/wall-{self.owner.vk_id}_{self.id}'
        super(VKPost, self).save(*args, **kwargs)


class Publication(models.Model):
    author = models.CharField(max_length=MAX_LENGTH)
    link = models.URLField()
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=MAX_LENGTH)
    text = models.TextField()

    def __str__(self):
        return f'{self.author}| {self.title}'