import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Phrase, Topic, SubTopic

def delete_file_if_needed(instance, field_name):
    try:
        old_file = getattr(instance.__class__.objects.get(pk=instance.pk), field_name)
    except instance.__class__.DoesNotExist:
        return

    new_file = getattr(instance, field_name)
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(pre_save, sender=Phrase)
def auto_delete_old_files_on_change(sender, instance, **kwargs):
    delete_file_if_needed(instance, 'image_2d')
    delete_file_if_needed(instance, 'image_3d')
    delete_file_if_needed(instance, 'audio_de')
    delete_file_if_needed(instance, 'audio_ru')
    delete_file_if_needed(instance, 'audio_ua')
    delete_file_if_needed(instance, 'audio_ar')
    delete_file_if_needed(instance, 'audio_fa')

@receiver(post_delete, sender=Phrase)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    for field in ['image_2d', 'image_3d', 'audio_de', 'audio_ru', 'audio_ua', 'audio_ar', 'audio_fa']:  # adjust fields as needed
        file = getattr(instance, field, None)
        if file and os.path.isfile(file.path):
            os.remove(file.path)

# If Topic or SubTopic have file fields, you can duplicate similar logic:
@receiver(post_delete, sender=Topic)
@receiver(post_delete, sender=SubTopic)
def delete_related_files(sender, instance, **kwargs):
    for field in ['image_2d', 'image_3d']:  # adjust field names based on your models
        file = getattr(instance, field, None)
        if file and os.path.isfile(file.path):
            os.remove(file.path)

@receiver(pre_save, sender=Topic)
@receiver(pre_save, sender=SubTopic)
def auto_delete_old_files_on_change(sender, instance, **kwargs):
    delete_file_if_needed(instance, 'image_2d')
    delete_file_if_needed(instance, 'image_3d')

@receiver(pre_save, sender=SubTopic)
def update_phrase_topic_on_subtopic_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = SubTopic.objects.get(pk=instance.pk)
    except SubTopic.DoesNotExist:
        return

    if old_instance.topic_id != instance.topic_id:
        Phrase.objects.filter(subtopic=instance).update(topic=instance.topic)

@receiver(post_delete, sender=SubTopic)
def delete_phrases_with_subtopic(sender, instance, **kwargs):
    Phrase.objects.filter(subtopic=instance).delete()

@receiver(post_delete, sender=Topic)
def delete_phrases_with_topic(sender, instance, **kwargs):
    Phrase.objects.filter(topic=instance).delete()  