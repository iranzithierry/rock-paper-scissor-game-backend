from django.urls import path

from src.games.asgi.consumers import  GameConsumer

websocket_urlpatterns = [
    path("ws/game/<game_id>/", GameConsumer.as_asgi()),
]
