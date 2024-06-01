from rest_framework.routers import SimpleRouter

from src.games.views import GameViewSet

games_router = SimpleRouter()

games_router.register(r'games', GameViewSet)
