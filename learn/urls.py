# learn/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TopicViewSet, SubTopicViewSet, PhraseViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'phrases', PhraseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
