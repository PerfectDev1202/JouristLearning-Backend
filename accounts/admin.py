from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, NotificationSettings

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_verified', 'is_premium', 'is_active', 'role')
    list_filter = ('country', 'primary_language', 'foreign_language')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'is_verified', 'is_premium', 'avatar', 'country', 'city', 'primary_language', 'foreign_language', 'ui_language', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)

class NotificationSettingsAdmin(admin.ModelAdmin):  
    model = NotificationSettings
    list_display = ('user', 'email_notifications', 'push_notifications', 'learning_reminders', 'weekly_progress', 'new_features', 'marketing')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NotificationSettings, NotificationSettingsAdmin)

