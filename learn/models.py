from django.db import models
from accounts.models import CustomUser
import uuid

LANGUAGES = ['de', 'ru', 'ua', 'ar', 'fa']

def image3d_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"images/3d/{filename}"

def image2d_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"images/2d/{filename}"

class Topic(models.Model):
    de = models.CharField(max_length=255, null=True, blank=True)
    ru = models.CharField(max_length=255, null=True, blank=True)
    ua = models.CharField(max_length=255, null=True, blank=True)
    ar = models.CharField(max_length=255, null=True, blank=True)
    fa = models.CharField(max_length=255, null=True, blank=True)

    contentID = models.CharField(max_length=255, null=True, blank=True)

    image_2d = models.ImageField(upload_to=image2d_upload_path, null=True, blank=True)
    image_3d = models.ImageField(upload_to=image3d_upload_path, null=True, blank=True)
    is_shared = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='topics')

    def __str__(self):
        return str(self.pk)

class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    de = models.CharField(max_length=255, null=True, blank=True)
    ru = models.CharField(max_length=255, null=True, blank=True)
    ua = models.CharField(max_length=255, null=True, blank=True)
    ar = models.CharField(max_length=255, null=True, blank=True)
    fa = models.CharField(max_length=255, null=True, blank=True)

    contentID = models.CharField(max_length=255, null=True, blank=True)

    image_2d = models.ImageField(upload_to=image2d_upload_path, null=True, blank=True)
    image_3d = models.ImageField(upload_to=image3d_upload_path, null=True, blank=True)
    is_shared = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='subtopics')

    def __str__(self):
        return str(self.pk)

class Phrase(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='phrases')
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='phrases')

    contentID = models.CharField(max_length=255, null=True, blank=True)

    de = models.TextField(null=True, blank=True)
    ru = models.TextField(null=True, blank=True)
    ua = models.TextField(null=True, blank=True)
    ar = models.TextField(null=True, blank=True)
    fa = models.TextField(null=True, blank=True)
    
    audio_de = models.FileField(upload_to='audio/de/', null=True, blank=True)
    audio_ru = models.FileField(upload_to='audio/ru/', null=True, blank=True)
    audio_ua = models.FileField(upload_to='audio/ua/', null=True, blank=True)
    audio_ar = models.FileField(upload_to='audio/ar/', null=True, blank=True)
    audio_fa = models.FileField(upload_to='audio/fa/', null=True, blank=True)

    image_2d = models.ImageField(upload_to=image2d_upload_path, null=True, blank=True)
    image_3d = models.ImageField(upload_to=image3d_upload_path, null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='phrases')

    def __str__(self):
        return str(self.pk)
