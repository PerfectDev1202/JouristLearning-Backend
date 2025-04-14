# learn/views.py

from rest_framework import viewsets
from .models import Topic, SubTopic, Phrase
from .serializers import TopicSerializer, SubTopicSerializer, PhraseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SubTopicViewSet(viewsets.ModelViewSet):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
