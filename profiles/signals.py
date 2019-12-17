from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.conf import settings
# from rest_framework.authtoken.models import Token

from .models import Profile

@receiver(post_save, sender = User)
def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user = instance)



@receiver(pre_save, sender = Profile)
def pre_save_profile(sender, instance, *args, **kwargs):
    if not instance.username:
        instance.username = instance.user.username


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
