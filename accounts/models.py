from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
import os
from django.utils.text import slugify

# Custom avatar path
def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.email)}-{uuid.uuid4().hex}.{ext}"
    return f"avatars/{filename}"

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError('Superusers must have a password.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusers must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusers must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    primary_language = models.CharField(max_length=50, blank=True, null=True)
    foreign_language = models.CharField(max_length=50, blank=True, null=True)
    ui_language = models.CharField(max_length=50, default='en')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class NotificationSettings(models.Model):
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    learning_reminders = models.BooleanField(default=True)
    weekly_progress = models.BooleanField(default=True)
    new_features = models.BooleanField(default=True)
    marketing = models.BooleanField(default=False)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_settings', primary_key=True)

    def __str__(self):
        return f"{self.user.email} Notification Settings"
