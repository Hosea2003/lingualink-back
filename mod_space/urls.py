from . import views
from django.urls import path

urlpatterns = [
    path('available-languages', views.available_languages),
    path('create-room', views.create_room),
    path('insert-language/<int:pk>', views.insert_language),
    path('view-languages/<int:pk>', views.room_available_languages),
    path('view-room/<str:slug>', views.view_room)
]