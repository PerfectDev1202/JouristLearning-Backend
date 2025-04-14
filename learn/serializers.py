# learn/serializers.py

from rest_framework import serializers
from .models import Topic, SubTopic, Phrase

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = '__all__'

class PhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = '__all__'
