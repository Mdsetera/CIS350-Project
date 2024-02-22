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
        self.table_cards = []
        self.seat = []
        self.active_players = []
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

            for player in self.seat:
                if player.chips > 0:
                    self.active_players.append(player)

            ##deal initial cards to all active players
            #(optional)add deal animation here
            for x in range(2):
                for player in self.active_players:
                    player.hand.append(self.deck.stack[0])
                    self.deck.stack.pop(0)


            ##first round of bets

            ##starts with the blinds
            seat_turn = self.dealer_seat + 1
            if seat_turn >= len(self.seat): seat_turn = 0
            current_player = self.seat[seat_turn]

            if current_player in self.active_players:
                if len(self.active_players) == 2:
                    ##just do big blind
                    if current_player.chips < self.big_blind:
                        current_player.bet = current_player.chips
                        current_player.all_in = True
                        self.highest_bet = current_player.bet
                else:
                    #do small and big blind
                    #small
                    if current_player.chips < self.sml_blind:
                        current_player.bet = current_player.chips
                        current_player.all_in = True
                        self.highest_bet = current_player.bet
                    else:
                        current_player.bet = self.sml_blind
                    current_player.chips -= current_player.bet

                    #switch current player
                    current_player = self.next_player(current_player)

                    #big
                    if current_player.chips < self.big_blind:
                        current_player.bet = current_player.chips
                        current_player.all_in = True
                    else:
                        current_player.bet = self.big_blind
                    current_player.chips -= current_player.bet
                    if current_player.bet > self.highest_bet:
                        self.highest_bet = current_player.bet

            while (not self.equal_bets()):
                current_player._play()#FIX ME: need to recieve player input

            ##second round of bets

    def next_player(self, current_player):
        #returns the player whos turn is next
        index = self.active_players.index(current_player)
        if index == len(self.active_players) - 1:
            current_player = self.active_players[0]
        else:
            current_player = self.active_players[index + 1]
        return current_player


    def equal_bets(self):
        #sent a list of players, returns True if all bets are equal to the highest bet
        for player in self.active_players:
            if player.bet != self.highest_bet and (player.all_in == False):
                    return False
        return True
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
        elif x == 1:
            return True
        return False
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
            x = random.randint(0, num_cards-1)
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
    def _play(self, game:Game) -> bool :
        """
        Will control each turn that the player takes
        player input = {0:_fold, 1:_call, 2:_bet}
        """
        return False
    def _bet(self, game:Game, amount:int):
        """
        player bets an amount of their chips,
        you must bet at least double the big blind, if you do not have enough chips then call()
        if you are in the lead, the highest amount you can bet is as much as the next highest player
        """
        if amount > self.chips:
            raise ValueError('player cannot bet more than you have')
        elif amount < 0:
            raise ValueError('player cannot bet less than 0')
        elif (self.bet + self.chips) < self.get_bet_range(game)[0]:#player cannot bet if they cannot match highest bet
            raise ValueError('player cannot meet minimum bet amount')
        else:
            self.bet += amount
            self.chips -= amount

        return False
    def get_bet_range(self, game:Game) -> (int,int):
        highest_chip_count = 0
        second_highest_chip_count = 0
        for player in game.active_players:
            if player.chips > highest_chip_count:
                second_highest_chip_count = highest_chip_count
                highest_chip_count = player.chips
        max_bet = 0
        if self.chips == highest_chip_count:
            max_bet = second_highest_chip_count
        else:
            max_bet = self.chips

        min_bet = game.highest_bet + game.big_blind

        return min_bet, max_bet
    def _fold(self, game:Game):
        """
        player ends involvement in the round and forfeits eligibility to the pot
        """
    def _call(self, game:Game):
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
