# game_logic.py
import random

class RPSGame:
    def __init__(self):
        self.choices = ["Rock", "Paper", "Scissors"]
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.winner = None

    def make_computer_choice(self):
        self.computer_choice = random.choice(self.choices)

    def determine_winner(self):
        if self.player_choice == self.computer_choice:
            self.winner = "It's a Tie!"
        elif (self.player_choice == "Rock" and self.computer_choice == "Scissors") or \
             (self.player_choice == "Scissors" and self.computer_choice == "Paper") or \
             (self.player_choice == "Paper" and self.computer_choice == "Rock"):
            self.winner = "You Win!"
            self.player_score += 1
        else:
            self.winner = "Computer Wins!"
            self.computer_score += 1

    def reset_round(self):
        self.player_choice = None
        self.computer_choice = None
        self.winner = None
