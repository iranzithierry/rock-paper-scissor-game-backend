from app.games.models import Game, Choice, Interaction
def determine_winner(game: Game):     
    choices = Choice.objects.filter(game=game)
    choices_theory = {'rock': 'scissor', 'scissor': 'paper', 'paper': 'rock'}
    if choices and game.both_played():
        if  choices[0].choice == choices[1].choice:
            return "Tie"
        elif choices_theory[choices[0].choice] == choices[1].choice:
            return choices[0].player
        else:
            return choices[1].player
    return None