from rest_framework import viewsets, mixins
from rest_framework.permissions import  IsAuthenticated


from src.games.models import Game
from src.games.serializers import GameSerializer


class GameViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Get,  Create and Retrieve- Game
    """
    

    queryset = Game.objects.all()
    serializers = {'default': GameSerializer}
    permissions = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
