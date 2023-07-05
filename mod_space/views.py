from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from mod_space.models import Room, RoomLanguage
from mod_space.serializers import RoomSerializer, RoomLanguageSerializer
from mod_space.utils import room_owner, load_languages, check_language_code, allow_to_view
from mod_user.models import LinguaUser


@api_view(["GET"])
def available_languages(request):
    languages=load_languages()
    return Response(languages)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_room(request: Request):
    data = request.data
    user = request.user

    serializer = RoomSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors)

    room = Room.objects.create(
        host=user,
        name=data.pop("name"),
        **data
    )

    return Response(RoomSerializer(room).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@room_owner
def insert_language(request: Request,pk):
    language_code=request.data.get("language_code")
    translator_id = request.data.get("translator_id")
    room=get_object_or_404(Room, pk=pk)

    language = check_language_code(language_code)
    if not language:
        return Response("Language code doesn't exist", status=status.HTTP_404_NOT_FOUND)

    translator = get_object_or_404(LinguaUser, pk=translator_id)

    #   if language_code already in room_language
    exist = RoomLanguage.objects.filter(room=room, language_code=language_code).first()

    if exist:
        return Response({"message":"This language already exist"})

    room_language=RoomLanguage.objects.create(
        room=room,
        translator=translator,
        language_code=language_code
    )

    return Response(RoomLanguageSerializer(room_language).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@allow_to_view
def room_available_languages(request:Request, pk):
    room = get_object_or_404(Room, pk=pk)
    languages = room.languages.all()
    return Response(RoomLanguageSerializer(languages, many=True).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_room(request, slug:str):
    room = get_object_or_404(Room, slug=slug)
    return redirect("/room/view-languages/%s"%str(room.id))
