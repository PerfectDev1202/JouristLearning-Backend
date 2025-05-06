# learn/serializers.py

from rest_framework import serializers
from .models import Topic, SubTopic, Phrase

class TopicSerializer(serializers.ModelSerializer):
    subtopic_count = serializers.IntegerField(read_only=True)
    phrase_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Topic
        fields = ['id', 'de', 'ru', 'ua', 'ar', 'fa', 'image_2d', 'image_3d', 'is_shared', 'owner', 'subtopic_count', 'phrase_count']

class SubTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), write_only=True, source='topic'
    )
    class Meta:
        model = SubTopic
        fields = '__all__'

class PhraseSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    subtopic = SubTopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), write_only=True, source='topic'
    )
    subtopic_id = serializers.PrimaryKeyRelatedField(
        queryset=SubTopic.objects.all(), write_only=True, source='subtopic'
    )
    class Meta:
        model = Phrase
        fields = '__all__'
