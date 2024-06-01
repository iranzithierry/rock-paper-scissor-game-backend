from rest_framework import serializers
from .models import Game, Interaction
from src.users.serializers import PlayerSerializer

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'mode',
            'status',
            'timestamp',
        )
    def to_representation(self, instance: Game):
        representation = super().to_representation(instance)
        players = [
            {**PlayerSerializer(interaction.player).data,
            } for interaction in Interaction.objects.filter(game=instance)
        ]
        representation["players"] = players
        return representation