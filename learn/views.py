# learn/views.py

from rest_framework import viewsets
from .models import Topic, SubTopic, Phrase
from .serializers import TopicSerializer, SubTopicSerializer, PhraseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .serializers import TopicSerializer
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


import json
import os
import re
import requests

de_path = "https://de.jourist.com/download/development/de_mp3.zip"
ru_path = "https://de.jourist.com/download/development/ru_mp3.zip"
ua_path = "https://de.jourist.com/download/development/ua_mp3.zip"
ar_path = "https://de.jourist.com/download/development/ar_mp3.zip"
fa_path = "https://de.jourist.com/download/development/fa_mp3.zip"



@api_view(['GET'])
@permission_classes([AllowAny])
def test_view(request):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Open the JSON file and load its contents
    with open(os.path.join(current_directory, 'data.json'), 'r') as file:
        data = json.load(file)

    # for item in data:
    #     if item.get("Topics") == 'MAIN':
    #         topic = Topic.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             image_3d="images/3d/" + item.get("ID") + ".png",
    #             is_shared=True
    #         )
    #         print(f"Created Topic: {topic.id}")

    #         TopicSerializer(topic)

    # for item in data:
    #     if item.get("Topics") == 'SUB':
    #         topic_id = item.get("ID").split(".")[0]
            
    #         topic = SubTopic.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             image_3d="images/3d/" + item.get("ID") + "png",
    #             topic=Topic.objects.get(id=(int(topic_id)+32)),
    #             is_shared=True
    #         )
    #         print(f"Created Topic: {topic.id}")

    #         TopicSerializer(topic)
    
    # for item in data:
    #     if item.get("Topics") == '':
    #         subtopic_ID = item.get("ID").split(".")[0]+ '.' + item.get("ID").split(".")[1]+'.'
    #         print(subtopic_ID)

    #         # subtopic_de = ''
    #         for x in data:
    #             if x.get("ID") == subtopic_ID:
    #                 subtopic_de = x.get("de")
    #                 break

    #         subtopic = SubTopic.objects.filter(de=subtopic_de).first()
            
    #         phrase = Phrase.objects.create(
    #             de=item.get("de"),
    #             ru=item.get("ru"),
    #             ua=item.get("ua"),
    #             ar=item.get("ar"),
    #             fa=item.get("fa"),
    #             image_3d="images/3d/" + item.get("ID") + ".png",
    #             subtopic=subtopic,
    #             is_shared=True
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



    return Response({"message": "This is a public test endpoint"}, status=status.HTTP_200_OK)