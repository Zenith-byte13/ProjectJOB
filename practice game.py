import random


def get_choices():
    player_choice = input( "Input a Choice - rock, paper, scissor:")
    options = ["rock", "paper", "scissors"]
    computer_choice = random.choice(options)
    choices = { "player" : player_choice , "computer" : computer_choice}
    return choices

def check_win(player, computer):
    print(f"\nYou chose: {player} \nComputer chose: {computer} ") 
    if player == computer:
        return "It's a Tie!"
    elif player == "rock": #1
        if computer == "scissors":
            return "Rock Wins! You Win!"
        else:
            return "Paper Wins! You Lose!"
    elif player == "paper": #2
        if computer == "rock":
            return "Paper Wins! You Win!"
        else:
            return "Scissors Wins! You Lose!"
    elif player == "scissors": #3
        if computer == "paper":
            return "Scissors Wins! You Win!"
        else:
            return "Rock Wins! You Lose!"
        
choices = get_choices()   
result = check_win(choices["player"], choices["computer"])
print(result)

