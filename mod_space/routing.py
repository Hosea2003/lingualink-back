from django.urls import path
from .consumers.message_consumer import MessageConsumer

websocket_urlpatterns=[
    path('room/<str:slug>/<str:code>', MessageConsumer.as_asgi())
]