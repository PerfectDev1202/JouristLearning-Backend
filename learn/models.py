from django.db import models
from accounts.models import CustomUser

LANGUAGES = ['de', 'ru', 'ua', 'ar', 'fa']

class Topic(models.Model):
    de = models.CharField(max_length=255)
    ru = models.CharField(max_length=255)
    ua = models.CharField(max_length=255)
    ar = models.CharField(max_length=255)
    fa = models.CharField(max_length=255)

    image_2d = models.ImageField(upload_to='images/2d/', null=True, blank=True)
    image_3d = models.ImageField(upload_to='images/3d/', null=True, blank=True)
    is_shared = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='topics')

    def __str__(self):
        return self.de

class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    de = models.CharField(max_length=255)
    ru = models.CharField(max_length=255)
    ua = models.CharField(max_length=255)
    ar = models.CharField(max_length=255)
    fa = models.CharField(max_length=255)

    image_2d = models.ImageField(upload_to='images/2d/', null=True, blank=True)
    image_3d = models.ImageField(upload_to='images/3d/', null=True, blank=True)
    is_shared = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='subtopics')

    def __str__(self):
        return self.de

class Phrase(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='phrases')
    de = models.TextField()
    ru = models.TextField()
    ua = models.TextField()
    ar = models.TextField()
    fa = models.TextField()
    
    audio_de = models.FileField(upload_to='audio/de/', null=True, blank=True)
    audio_ru = models.FileField(upload_to='audio/ru/', null=True, blank=True)
    audio_ua = models.FileField(upload_to='audio/ua/', null=True, blank=True)
    audio_ar = models.FileField(upload_to='audio/ar/', null=True, blank=True)
    audio_fa = models.FileField(upload_to='audio/fa/', null=True, blank=True)

    image_2d = models.ImageField(upload_to='images/2d/', null=True, blank=True)
    image_3d = models.ImageField(upload_to='images/3d/', null=True, blank=True)
    is_shared = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='phrases')

    def __str__(self):
        return self.de
