# learn/serializers.py

from rest_framework import serializers
from .models import Topic, SubTopic, Phrase

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    class Meta:
        model = SubTopic
        fields = '__all__'

class PhraseSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    subtopic = SubTopicSerializer(read_only=True)
    class Meta:
        model = Phrase
        fields = '__all__'
