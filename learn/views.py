# learn/views.py

from rest_framework import viewsets
from django.conf import settings
from .models import Topic, SubTopic, Phrase
from .serializers import TopicSerializer, SubTopicSerializer, PhraseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

import random
from .serializers import TopicSerializer
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]
class SubTopicViewSet(viewsets.ModelViewSet):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer
    permission_classes = [IsAuthenticated]
class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = [IsAuthenticated]


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
@permission_classes([AllowAny])
def get_shared_subtopics_by_topic(request, topic_id):
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


import json
import os
import re
import requests

@api_view(['GET'])
@permission_classes([AllowAny])
def get_missing_phrase_3d_files(request):
    phrases_with_paths = Phrase.objects.filter(is_shared=True).exclude(image_3d__isnull=True).exclude(image_3d='')
    subtopics_with_paths = SubTopic.objects.filter(is_shared=True).exclude(image_3d__isnull=True).exclude(image_3d='')
    topics_with_paths = Topic.objects.filter(is_shared=True).exclude(image_3d__isnull=True).exclude(image_3d='')

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