# learn/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TopicViewSet, SubTopicViewSet, PhraseViewSet, test_view, get_random_shared_phrases, get_missing_phrase_3d_files, get_shared_topics, get_shared_subtopics_by_topic, get_shared_subtopic_by_id, get_shared_phrases_by_subtopic

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'phrases', PhraseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', test_view, name='test'),
    path('random-phrases/', get_random_shared_phrases, name='random-phrases'),
    path('missing-files/', get_missing_phrase_3d_files, name='missing-files'),
    path('shared-topics/', get_shared_topics, name='shared-topics'),
    path('shared-subtopics/<int:topic_id>/', get_shared_subtopics_by_topic, name='shared-subtopics-by-topic'),
    path('shared-subtopic/<int:subtopic_id>/', get_shared_subtopic_by_id, name='shared-subtopic-by-id'),
    path('shared-phrases/<int:subtopic_id>/', get_shared_phrases_by_subtopic, name='shared-phrases-by-subtopic'),
]
