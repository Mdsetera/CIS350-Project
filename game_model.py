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
    def __init__(self, num_User_players = 3, num_AI_players = 0):
        self.deck = Deck()
        self.seat = []
        self.pot = []
        self.highest_bet = 0
        self.sml_blind = 10
        self.big_blind = 20

        self.dealer_seat = 0

        for x in range(num_User_players):#add user players
            self.seat.append(UserPlayer())
        for x in range(num_AI_players):#add AI players
            self.seat.append(AIPlayer())

        ##everyone is now seated at the table


        self.round = 0 ##blind amount should increase every five founds
        while(self.checkEndGame()==False):
            self.round += 1

            active_players = [] #players participating in the current hand
            for player in self.seat:
                if player.chips > 0:
                    active_players.append(player)

            ##deal initial cards to all active players
            #(optional)add deal animation here
            for x in range(2):
                for player in active_players:
                    player.hand.append(self.deck.stack[0])
                    self.deck.stack.pop(0)


            ##first round of bets

            ##second round of bets


    @property
    def dealer_seat(self):
        return self._dealer_seat
    @dealer_seat.setter
    def dealer_seat(self, num):
        if num == len(self.seat):
            self._dealer_seat = 0
        elif num < 0:
            raise ValueError('dealer seat cannot be < 0')
        elif num > len(self.seat):
            raise ValueError('invalid dealer seat')
        else:
            self._dealer_seat = num
    def checkEndGame(self) -> bool:
        #checks all players chip count,
        x = 0
        for player in self.seat:
            if player.chips > 0:
                x += 1
        if x == 0:
            raise ValueError('at least one player must have chips')

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
        self.width = self.rect.width
        self.height = self.rect.height

    def __repr__(self):
        return f'{self.value},{self.suit},'

class Player:
    def __init__(self):
        self.hand = []
        self.chips = 1000
        self.hand_rank = None
        self.bet = 0
        self.pot_eligibility = 0
        self.winnings = 0
        self.all_in = False
    @property
    def chips(self):
        return self._chips

    @chips.setter
    def chips(self, num):
        if num < 0:
            raise ValueError('chip count cannot be < 0')
        elif num % 5 != 0:
            raise ValueError('chip count must be a multiple of 5')
        else:
            self._chips = num
    def _play(self) -> bool :
        """
        Will control each turn that the player takes
        """
        return False
    def _bet(self, amount:int):
        """
        player bets an amount of their chips,
        you must bet at least double the big blind, if you do not have enough chips then call()
        if you are in the lead, the highest amount you can bet is as much as the next highest player
        """
        return False
    def _fold(self):
        """
        player ends involvement in the round and forfeits eligibility to the pot
        """
    def _call(self):
        """
        player matches the highest bet on the table
        if highest bet is more than player has, player calls with all their chips and goes 'all-in'
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
