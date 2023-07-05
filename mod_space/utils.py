from django.http import HttpResponse

from mod_space.models import Room, RoomInvitation

import json
import os
from django.conf import settings
from django.shortcuts import get_object_or_404


def room_owner(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        pk = kwargs.get("pk")
        room = Room.objects.filter(pk=pk, host=user).first()
        if not room:
            return HttpResponse("You are not the owner", status=401)
        return func(request, *args, **kwargs)

    return wrapper


def allow_to_view(func):
    def wrapper(request, *args, **kwargs):
        pk = kwargs.get("pk")
        user = request.user
        room = get_object_or_404(Room, pk=pk)
        if room.type_of == Room.OPEN_TO_ALL or (
                user == room.host or RoomInvitation.objects.filter(user=user, room=room)
        ):
            return func(request, *args, **kwargs)

        return HttpResponse("You are not allowed to view", status=401)

    return wrapper


def load_languages():
    file = open(os.path.join(settings.BASE_DIR, "languages.json"))
    languages = json.load(file)
    return languages


def check_language_code(code):
    for language in load_languages():
        if language.get("code") == code:
            return language
    return None
