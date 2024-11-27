from django.urls import path
from .consumers import ChatConsumer
from . import views

urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
    # path("ws/chats", views.list_chats),
]
