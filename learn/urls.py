# learn/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TopicViewSet, SubTopicViewSet, PhraseViewSet, test_view

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'phrases', PhraseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', test_view, name='test'),
]
