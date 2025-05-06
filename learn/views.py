# learn/views.py

from rest_framework import viewsets
from django.conf import settings
from .models import Topic, SubTopic, Phrase
from .serializers import TopicSerializer, SubTopicSerializer, PhraseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, Prefetch
import os
import random
from .serializers import TopicSerializer
import json
from constants import BACKEND_URL


data_json = json.load(open(os.path.join(settings.BASE_DIR, 'learn', 'data.json')))
filtered_phrases = [d for d in data_json if d.get("Topics") == ""]
filtered_phrases_question_marks = [d for d in filtered_phrases if "?" in d.get("de") ]
filtered_phrases_emotion_marks = [d for d in filtered_phrases if "!" in d.get("de") ]
filtered_phrases_no_marks = [d for d in filtered_phrases if "?" not in d.get("de") and "!" not in d.get("de") ]


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        topic = self.get_object()
        if topic.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this topic.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            primary_language = user.primary_language or 'de'    
            foreign_language = user.foreign_language or 'ua'

            primary_language_filter = {f'{primary_language}__isnull': False}
            foreign_language_filter = {f'{foreign_language}__isnull': False}

            return Topic.objects.filter(Q(owner=user) | Q(is_shared=True), **primary_language_filter, **foreign_language_filter).annotate(
            subtopic_count=Count(
                'subtopics',
                filter=Q(subtopics__owner=user) | Q(subtopics__is_shared=True),
                distinct=True
            ),
            phrase_count=Count(
                'phrases',
                filter=Q(phrases__owner=user) | Q(phrases__is_shared=True),
                distinct=True
            )
        )
        
        return Topic.objects.filter(is_shared=True).annotate(
            subtopics_count=Count(
                'subtopics',
                filter=Q(subtopics__is_shared=True),
                distinct=True
            ),
            phrases_count=Count(
                'phrases',
                filter=Q(phrases__is_shared=True),  # assuming 'is_shared' exists on Phrase
                distinct=True
            )
        )

class SubTopicViewSet(viewsets.ModelViewSet):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        subtopic = self.get_object()
        if subtopic.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this subtopic.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)

class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        phrase = self.get_object()
        if phrase.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this phrase.'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)
            
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Phrase.objects.filter(Q(owner=user) | Q(is_shared=True))
        return Phrase.objects.filter(is_shared=True)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_topics(request):
    user = request.user
    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    topics = Topic.objects.filter(Q(owner=user) | Q(is_shared=True), **primary_language_filter, **foreign_language_filter).annotate(
        subtopic_count=Count('subtopics', filter=Q(Q(subtopics__owner=user) | Q(subtopics__is_shared=True)), distinct=True),
        phrase_count=Count('phrases', filter=Q(Q(phrases__owner=user)), distinct=True)
    ).prefetch_related(
        Prefetch(
            'subtopics',
            queryset=SubTopic.objects.filter(Q(owner=user) | Q(is_shared=True)).prefetch_related('phrases'),
            to_attr='filtered_subtopics'
        )
    )

    data = []
    for topic in topics:
        serialized = TopicSerializer(topic).data
        serialized['subtopic_count'] = topic.subtopic_count
        serialized['phrase_count'] = topic.phrase_count

        subtopics = getattr(topic, 'filtered_subtopics', [])
        subtopic_data = []

        for subtopic in subtopics:
            sub_serialized = SubTopicSerializer(subtopic).data
            phrase_count = subtopic.phrases.filter(owner=user).count()
            sub_serialized['phrase_count'] = phrase_count
            subtopic_data.append(sub_serialized)

        serialized['subtopics'] = subtopic_data
        data.append(serialized)

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_phrases_by_subtopic(request, subtopic_id):
    user = request.user
    phrases = Phrase.objects.filter(Q(owner=user), subtopic_id=subtopic_id)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append(serialized)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_phrase_by_topic(request, topic_id):
    user = request.user
    phrases = Phrase.objects.filter(Q(owner=user), topic_id=topic_id)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append(serialized)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_subtopics_by_topic(request, topic_id):
    user = request.user
    subtopics = SubTopic.objects.filter(Q(owner=user) | Q(is_shared=True), topic_id=topic_id)
    data = []
    for subtopic in subtopics:
        serialized = SubTopicSerializer(subtopic).data
        data.append(serialized)
    return Response(data)

######################### exercise endpoints. =========================================>
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_phrases_memorization(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append(serialized)

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_phrases_match(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        random_idx = random.choice([1,2,3,4])

        image_data = []

        for idx in [1,2,3,4]:
            if idx == random_idx:
                image_data.append({"id": idx, "src": BACKEND_URL + serialized[f"image_3d"], "correct": True})
            else:
                randomly_selected_data = random.choice(filtered_phrases)
                image_data.append({ "id": idx, "src": BACKEND_URL + "media/images/3d/" + randomly_selected_data.get("ID") + ".png", "correct": False})

        data.append({ 'id': phrase.id, "phrase": serialized[foreign_language], "audio": BACKEND_URL + serialized["audio_" + foreign_language], "images": image_data })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_forward_translation(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        options = []

        primary_language_phrase = serialized[primary_language]

        if "?" in primary_language_phrase:
            options.append(random.choice(filtered_phrases_question_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_question_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_question_marks).get(foreign_language))
        elif "!" in primary_language_phrase:
            options.append(random.choice(filtered_phrases_emotion_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_emotion_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_emotion_marks).get(foreign_language))
        else:
            options.append(random.choice(filtered_phrases_no_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_no_marks).get(foreign_language))
            options.append(random.choice(filtered_phrases_no_marks).get(foreign_language))
        
        options.append(serialized[foreign_language])
        
        data.append({
            "id": phrase.id,
            "phrase": serialized[primary_language],
            "correctTranslation": serialized[foreign_language],
            "image": BACKEND_URL + serialized["image_3d"],
            "options": random.sample(options, 4)
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_backward_translation(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        options = []

        foreign_language_phrase = serialized[foreign_language]

        if "?" in foreign_language_phrase:
            options.append(random.choice(filtered_phrases_question_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_question_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_question_marks).get(primary_language))
        elif "!" in foreign_language_phrase:
            options.append(random.choice(filtered_phrases_emotion_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_emotion_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_emotion_marks).get(primary_language))
        else:
            options.append(random.choice(filtered_phrases_no_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_no_marks).get(primary_language))
            options.append(random.choice(filtered_phrases_no_marks).get(primary_language))
        
        options.append(serialized[primary_language])
        
        data.append({
            "id": phrase.id,
            "phrase": serialized[foreign_language],
            "correctTranslation": serialized[primary_language],
            "image": BACKEND_URL + serialized["image_3d"],
            "options": random.sample(options, 4)
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_translation_guess(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append({
            "id": serialized.get("id"),
            "primaryLanguage": serialized.get(primary_language),
            "foreignLanguage": serialized.get(foreign_language),
            "image": BACKEND_URL + serialized["image_3d"],
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_dictation_challenge(request, subtopic_id):
    user = request.user

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), subtopic_id=subtopic_id, **primary_language_filter, **foreign_language_filter)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append({
            "id": serialized.get("id"),
            "foreignLanguage": serialized.get(foreign_language),
            "audio": BACKEND_URL + serialized.get("audio_" + foreign_language),
            "image": BACKEND_URL + serialized["image_3d"],
        })

    return Response(data)


######################## PDF Generation endpoints ===============================>
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subtopics_by_topics(request):
    user = request.user
    topics = request.query_params.get('topics', '[]')
    topics = json.loads(topics)

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    subtopics = SubTopic.objects.filter(Q(owner=user) | Q(is_shared=True), **primary_language_filter, **foreign_language_filter, topic_id__in=topics).annotate(
        phrase_count=Count('phrases', filter=Q(phrases__is_shared=True) | Q(phrases__owner=user), distinct = True)
    )
    data = []
    for subtopic in subtopics:
        serialized = SubTopicSerializer(subtopic).data
        data.append({
            "id": serialized.get("id"),
            "topicId": serialized.get("topic").get("id"),
            "primary": serialized.get(primary_language),
            "foreign": serialized.get(foreign_language),
            "imageUrl": BACKEND_URL + serialized["image_3d"],
            "phraseCount": subtopic.phrase_count,
        })

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phrases_by_subtopics(request):
    user = request.user
    subtopics = request.query_params.get('subtopics', '[]')
    subtopics = json.loads(subtopics)

    primary_language = user.primary_language or 'de'
    foreign_language = user.foreign_language or 'ua'

    primary_language_filter = {f'{primary_language}__isnull': False}
    foreign_language_filter = {f'{foreign_language}__isnull': False}

    phrases = Phrase.objects.filter(Q(owner=user) | Q(is_shared=True), **primary_language_filter, **foreign_language_filter, subtopic_id__in=subtopics)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append({
            "id": serialized.get("id"),
            "subtopicId": serialized.get("subtopic").get("id"),
            "primary": serialized.get(primary_language),
            "foreign": serialized.get(foreign_language),
            "imageUrl": BACKEND_URL + serialized["image_3d"],
        })

    return Response(data)








###########################################################################
###################### Public endpoints ###################################
###########################################################################
@api_view(['GET'])
@permission_classes([AllowAny])
def get_shared_phrases_by_subtopic(request, subtopic_id):
    phrases = Phrase.objects.filter(subtopic_id=subtopic_id, is_shared=True)
    data = []
    for phrase in phrases:
        serialized = PhraseSerializer(phrase).data
        data.append(serialized)

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_subtopics_by_topic(request, topic_id):
    user = request.user

    if user.is_authenticated:
        subtopics = SubTopic.objects.filter(Q(topic_id=topic_id) & (Q(is_shared=True) | Q(owner=user))).annotate(
            phrase_count=Count('phrases', filter=Q(phrases__is_shared=True) | Q(phrases__owner=user), distinct = True)
        )
    else:
        subtopics = SubTopic.objects.filter(topic_id=topic_id, is_shared=True).annotate(
            phrase_count=Count('phrases', filter=Q(phrases__is_shared=True, phrases__owner__isnull=True), distinct = True)
        )

    data = []
    for subtopic in subtopics:
        serialized = TopicSerializer(subtopic).data
        serialized['phrase_count'] = subtopic.phrase_count
        data.append(serialized)

    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_shared_subtopic_by_id(request, subtopic_id):
    subtopic = SubTopic.objects.filter(id=subtopic_id, is_shared=True).annotate(
        phrase_count=Count('phrases', filter=Q(phrases__is_shared=True, phrases__owner__isnull=True), distinct=True)
    ).first()
    if not subtopic:
        return Response({"error": "Subtopic not found"}, status=404)
    data = SubTopicSerializer(subtopic).data
    data['phrase_count'] = subtopic.phrase_count

    if data.get('is_shared'):
        return Response(data)
    else:
        return Response({"error": "Subtopic not found"}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_shared_topics(request):
    topics = Topic.objects.filter(is_shared=True).annotate(
        subtopic_count=Count('subtopics', filter=Q(subtopics__is_shared=True, subtopics__owner__isnull=True), distinct = True),
        phrase_count=Count('phrases', filter=Q(phrases__is_shared=True, phrases__owner__isnull=True), distinct = True)
    )
    data = []
    for topic in topics:
        serialized = TopicSerializer(topic).data
        serialized['subtopic_count'] = topic.subtopic_count
        serialized['phrase_count'] = topic.phrase_count
        data.append(serialized)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_random_shared_phrases(request):
    try:
        count = int(request.GET.get('count', 24))  # Default to 24 if not specified
    except ValueError:
        return Response({"error": "Invalid count parameter."}, status=400)

    total = Phrase.objects.count()
    if total == 0:
        return Response([])

    if count >= total:
        phrases = Phrase.objects.filter(is_shared=True)
    else:
        ids = list(Phrase.objects.filter(is_shared=True).values_list('id', flat=True))
        random_ids = random.sample(ids, count)
        phrases = Phrase.objects.filter(id__in=random_ids)

    serializer = PhraseSerializer(phrases, many=True)
    return Response(serializer.data)

















#######################################################################
#################  Test endpoints  ####################################
#######################################################################

@api_view(['GET'])
@permission_classes([AllowAny])
def get_missing_phrase_3d_files(request):
    phrases_with_paths = Phrase.objects.filter(is_shared=False).exclude(image_3d__isnull=True).exclude(image_3d='')
    subtopics_with_paths = SubTopic.objects.filter(is_shared=False).exclude(image_3d__isnull=True).exclude(image_3d='')
    topics_with_paths = Topic.objects.filter(is_shared=False).exclude(image_3d__isnull=True).exclude(image_3d='')

    missing = []

    for phrase in phrases_with_paths:
        file_path = os.path.join(settings.MEDIA_ROOT, str(phrase.image_3d))
        if not os.path.exists(file_path):
            missing.append(phrase.image_3d.name.split('/')[-1])

    for subtopic in subtopics_with_paths:
        file_path = os.path.join(settings.MEDIA_ROOT, str(subtopic.image_3d))
        if not os.path.exists(file_path):
            missing.append(subtopic.image_3d.name.split('/')[-1])
            
    for topic in topics_with_paths:
        file_path = os.path.join(settings.MEDIA_ROOT, str(topic.image_3d))
        if not os.path.exists(file_path):
            missing.append(topic.image_3d.name.split('/')[-1])

    return Response(missing)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_view(request):

    # Topic.objects.all().delete()
    # SubTopic.objects.all().delete()
    # Phrase.objects.all().delete()

    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # # Open the JSON file and load its contents
    # with open(os.path.join(current_directory, 'data.json'), 'r') as file:
    #     data = json.load(file)

    # for item in data:
    #     if item.get("Topics") == 'MAIN':
    #         topic = Topic.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             contentID=item.get("ID"),
    #             image_3d="images/3d/" + item.get("ID") + "png",
    #             is_shared=True
    #         )
    #         print(f"Created Topic: {topic.id}")

    #         TopicSerializer(topic)

    # for item in data:
    #     if item.get("Topics") == 'SUB':
    #         topic_id = item.get("ID").split(".")[0] + '.'
    #         topic = Topic.objects.filter(contentID=topic_id).first()
    #         if not topic:
    #             print(f"Topic not found: {topic_id}")
    #             continue
            
    #         subtopic = SubTopic.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             contentID=item.get("ID"),
    #             image_3d="images/3d/" + item.get("ID") + "png",
    #             topic=topic,
    #             is_shared=True
    #         )
    #         print(f"Created Subtopic: {subtopic.id}")

    #         SubTopicSerializer(subtopic)
    
    # for item in data:
    #     if item.get("Topics") == '':
    #         subtopic_ID = item.get("ID").split(".")[0]+ '.' + item.get("ID").split(".")[1]+'.'

    #         subtopic = SubTopic.objects.filter(contentID=subtopic_ID).first()
    #         if not subtopic:
    #             print(f"Subtopic not found: {subtopic_ID}")
    #             continue
            
    #         phrase = Phrase.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             contentID=item.get("ID"),
    #             image_3d="images/3d/" + item.get("ID") + ".png",
    #             subtopic=subtopic,
    #             topic=subtopic.topic,
    #             is_shared=True,
    #             audio_de = "audio/de/" + item.get("ID") + ".mp3",
    #             audio_ru = "audio/ru/" + item.get("ID") + ".mp3",
    #             audio_ua = "audio/ua/" + item.get("ID") + ".mp3",
    #             audio_ar = "audio/ar/" + item.get("ID") + ".mp3",
    #             audio_fa = "audio/fa/" + item.get("ID") + ".mp3",
    #         )

    #         PhraseSerializer(phrase)

    # for phrase in Phrase.objects.all():
    #     phrase_de = phrase.de
    #     print(phrase_de)

    #     for item in data:
    #         if item.get("de") == phrase_de:
    #             print(item.get("ID"))

    #             phrase.audio_de = "audio/de/" + item.get("ID") + ".mp3"
    #             phrase.audio_ru = "audio/ru/" + item.get("ID") + ".mp3"
    #             phrase.audio_ua = "audio/ua/" + item.get("ID") + ".mp3"
    #             phrase.audio_ar = "audio/ar/" + item.get("ID") + ".mp3"
    #             phrase.audio_fa = "audio/fa/" + item.get("ID") + ".mp3"

    #             phrase.save()


    # download the zip files
    # de_response = requests.get(de_path)
    # with open("de_mp3.zip", "wb") as file:
    #     file.write(de_response.content)

    # ru_response = requests.get(ru_path)
    # with open("ru_mp3.zip", "wb") as file:
    #     file.write(ru_response.content)

    # ua_response = requests.get(ua_path)
    # with open("ua_mp3.zip", "wb") as file:
    #     file.write(ua_response.content)

    # ar_response = requests.get(ar_path)
    # with open("ar_mp3.zip", "wb") as file:
    #     file.write(ar_response.content)

    # fa_response = requests.get(fa_path)
    # with open("fa_mp3.zip", "wb") as file:
    #     file.write(fa_response.content)

    # all_data = Topic.objects.all()
    # for item in all_data:
    #     if item.image_3d and ".." in item.image_3d.name:
    #         old_path = item.image_3d.name
    #         new_path = re.sub(r'\.+', '.', old_path)
    #         item.image_3d.name = new_path
    #         item.save()
    #         print(f"Updated: {old_path} ➜ {new_path}")

    # all_data = Phrase.objects.all()
    # for item in all_data:
    #     subtopic = item.subtopic
    #     topic = subtopic.topic

    #     item.topic = topic
    #     item.save()

    return Response({"message": "This is a public test endpoint"}, status=status.HTTP_200_OK)