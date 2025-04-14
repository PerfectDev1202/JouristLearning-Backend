from django.contrib import admin
from .models import Topic, SubTopic, Phrase

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'de', 'ru', 'ua', 'ar', 'fa', 'is_shared', 'owner')
    search_fields = ('de', 'ru', 'ua', 'ar', 'fa')

@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'de', 'ru', 'ua', 'ar', 'fa', 'is_shared', 'owner')
    search_fields = ('de', 'ru', 'ua', 'ar', 'fa')
    list_filter = ('topic',)

@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtopic', 'de', 'is_shared', 'owner')
    search_fields = ('de', 'ru', 'ua', 'ar', 'fa')
    list_filter = ('subtopic', 'is_shared')
