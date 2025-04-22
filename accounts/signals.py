# accounts/signals.py

import os
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import CustomUser, NotificationSettings


@receiver(pre_save, sender=CustomUser)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    if not instance.pk:
        # New user (no previous avatar to delete)
        return

    try:
        old_avatar = CustomUser.objects.get(pk=instance.pk).avatar
    except CustomUser.DoesNotExist:
        return

    new_avatar = instance.avatar
    if old_avatar and old_avatar != new_avatar:
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)


@receiver(post_delete, sender=CustomUser)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)

@receiver(post_save, sender=CustomUser)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.create(user=instance)