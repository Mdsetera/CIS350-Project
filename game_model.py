"""

CIS 350-01 Intro to Software Engineering
Term Project - Texas Hold'Em Poker - game_model.py
By: Austin Jackson, Caleb Taylor, Mitchell Setera

Description:
This project's goal is to recreate and design a Texas Hold'Em Poker
game. Features include a functional GUI, AI Players, and a tournament mode.
"""
import random
import copy
#import pygame as pg
from enum import Enum

import pygame


class Suit(Enum):
#determines the suit of each card
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4

class Game:
    def __init__(self, num_AI_players = 1):
        self.deck = Deck()
        self.seat = []
        self.pot = 0
        self.highest_bet = 0
        self.blind_amount = 50
        self.blind_seat = 1
        for x in range(num_AI_players):
            print("Eat shit")

class Deck:
    def __init__(self):
        self.stack = []
        self.populate()
        self.shuffle()

    def shuffle(self):
        #shuffle current cards in the deck
        new_deck = []
        num_cards = len(self.stack)
        while num_cards > 0:
            x = random.randint(0,num_cards-1)
            new_deck.append(self.stack[x])
            self.stack.pop(x)
            num_cards -= 1
        self.stack = new_deck

    def populate(self):
        #populates all cards into the deck, only used in __init__
        for x in range(2,15):
            self.stack.append(Card(x,Suit.HEARTS, "Images/card" + "Hearts" + str(x) + ".png"))
            self.stack.append(Card(x,Suit.DIAMONDS, "Images/card" + "Diamonds" + str(x) + ".png"))
            self.stack.append(Card(x,Suit.SPADES, "Images/card" + "Spades" + str(x) + ".png"))
            self.stack.append(Card(x,Suit.CLUBS, "Images/card" + "Clubs" + str(x) + ".png"))
    def __repr__(self):
        my_str = ""
        for card in self.stack:
            my_str += card.__repr__() + '\n'
        return my_str

class Card:
    def __init__(self, val: int, suit: Suit, image_path):
        self.suit = suit
        self.value = val
        self.front_image = pygame.image.load(image_path)
        self.back_image = pygame.image.load("Images/cardBack_red5.png")
        self.rect = self.front_image.get_rect()

    def __repr__(self):
        return f'{self.value},{self.suit}'

class Player:
    def __init__(self):
        self.hand = []
        self.chips = 1000
        self.hand_rank = None
        self.best_card = None
    def play(self) -> bool :
        """
        Will control each turn that the player takes
        """
        return False
    def bet(self, amount:int):
        """
        player bet an amount of their chips,
        check is the same as betting 0 chips
        you can only bet as much as at least one players has
        """
        return False
    def fold(self):
        """
        player ends involvement in the round and forfeits bets to the pot
        """
    def call(self):
        """
        player matches the highest bet on the table
        if highest bet is more than player has, player calls with all their chips
        """
    def check_hand_rank(self, hand:list[Card]) -> None:
        """
        given a hand of cards, returns the type of hand
        sets the hand rank and best card
        """
class UserPlayer(Player):
    def __init__(self):
        super().__init__()
    def play(self):
        """
        controls the turn of a user
        """
class AIPlayer(Player):
    def __init__(self):
        super().__init__()
    def play(self):
        """
        controls the turn of a AI player
        """


def main():
    deck = Deck()
    print(deck)
    print(len(deck.stack))

if __name__ == '__main__':
    main()
