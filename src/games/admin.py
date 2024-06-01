from django.contrib import admin
from src.games.models import Game, Interaction, Choice

# Register your models here.
admin.site.register(Game)
admin.site.register(Choice)
admin.site.register(Interaction)