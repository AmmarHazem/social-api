from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length = 300, unique = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'posts', on_delete = models.CASCADE)
    content = models.TextField()
    published = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(blank = True)

    class Meta:
        ordering = ('-created', 'title')

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'comments', on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment {self.id}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'likes', on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name = 'likes', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username}'
