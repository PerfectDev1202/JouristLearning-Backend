# learn/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TopicViewSet, SubTopicViewSet, PhraseViewSet, test_view, get_random_shared_phrases, get_missing_phrase_3d_files, get_shared_topics, get_all_subtopics_by_topic, get_shared_subtopic_by_id, get_shared_phrases_by_subtopic, get_user_topics, get_user_subtopics_by_topic, get_user_phrases_by_subtopic, get_user_phrase_by_topic, get_exercise_phrases_memorization, get_exercise_translation_guess, get_exercise_phrases_match, get_exercise_forward_translation, get_exercise_backward_translation, get_exercise_dictation_challenge, get_subtopics_by_topics, get_phrases_by_subtopics

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
    path('all-subtopics/<int:topic_id>/', get_all_subtopics_by_topic, name='all-subtopics-by-topic'),
    path('shared-subtopic/<int:subtopic_id>/', get_shared_subtopic_by_id, name='shared-subtopic-by-id'),
    path('shared-phrases/<int:subtopic_id>/', get_shared_phrases_by_subtopic, name='shared-phrases-by-subtopic'),
    path('user-topics/', get_user_topics, name='user-topics'),
    path('user-subtopics/<int:topic_id>/', get_user_subtopics_by_topic, name='user-subtopics-by-topic'),
    path('user-phrases-subtopic/<int:subtopic_id>/', get_user_phrases_by_subtopic, name='user-phrases-by-subtopic'),
    path('user-phrases-topic/<int:topic_id>/', get_user_phrase_by_topic, name='user-phrase-by-topic'),

    path('exercise-phrases-memorization/<int:subtopic_id>/', get_exercise_phrases_memorization, name='exercise-phrases-memorization'),
    path('exercise-phrases-match/<int:subtopic_id>/', get_exercise_phrases_match, name='exercise-phrases-match'),
    path('exercise-forward-translation/<int:subtopic_id>/', get_exercise_forward_translation, name='exercise-forward-translation'),
    path('exercise-backward-translation/<int:subtopic_id>/', get_exercise_backward_translation, name='exercise-backward-translation'),
    path('exercise-translation-guess/<int:subtopic_id>/', get_exercise_translation_guess, name='exercise-translation-guess'),
    path('exercise-dictation-challenge/<int:subtopic_id>/', get_exercise_dictation_challenge, name='exercise-dictation-challenge'),

    path('subtopics-by-topics/', get_subtopics_by_topics, name='subtopics-by-topics'),
    path('phrases-by-subtopics/', get_phrases_by_subtopics, name='phrases-by-subtopic'),
]
