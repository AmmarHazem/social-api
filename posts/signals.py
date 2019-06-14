from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify

import datetime

from .models import Post

@receiver(pre_save, sender = Post)
def post_save_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f'{slugify(instance.title)}-{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}'
