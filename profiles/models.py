from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from datetime import datetime

from posts.models import Post


def images_path(instance, filename):
    return f'user_{instance.user.id}/profile_images/{datetime.now().strftime("%Y-%m-%d")}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, blank = True)
    username = models.CharField(max_length = 200, editable = False, default = '')
    image = models.ImageField(images_path, null = True, blank = True)
    bio = models.TextField(blank = True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'followers', blank = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-created',)

    @property
    def posts(self):
        return self.user.posts.all()

    def __str__(self):
        return self.user.username

    def get_timeline(self):
        qs = Post.objects.none()
        for u in self.following.all():
            qs = qs | u.posts.all()
        return qs

    def get_absolute_url(self):
        return reverse_lazy('profiles:user-detail', kwargs = {'username' : self.__str__()})
