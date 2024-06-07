from django.urls import path
from app.games.consumers import GameConsumer

websocket_urlpatterns = [
    path("ws/game/<game_id>/", GameConsumer.as_asgi()),
]
