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
import poker_gui as gui


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
        self.current_player:Player = None
        self.pot = [0]
        self.highest_bet = 0
        self.sml_blind = 10
        self.big_blind = 20
        self.round = 0 ##blind amount should increase every five rounds
        self.bet_round = 0
        self.dealer_seat = 0
        self.screen, self.clock = gui.init_pygame()

        for x in range(num_User_players):#add user players
            self.seat.append(UserPlayer())
        for x in range(num_AI_players):#add AI players
            self.seat.append(AIPlayer())
        for player in self.seat:
            player.seat_number = self.seat.index(player)

        ##everyone is now seated at the table



    def start_round(self, screen):
        ##deal the cards
        self.round += 1
        self.screen = screen
        self.active_players = [player for player in self.seat if player.chips > 0]

        #self.take_first_round_bets()
        #self.update_pot()
        # if self.round == 1:
        #     self.take_bets(gui.show_flop, 3)
        #elif self.round == 2:
            #self.take_bets(gui.show_turn, 1)
        #elif self.round == 3:
            #self.take_bets(gui.show_river, 1)

    def deal_initial_cards(self):
        print('deal_initial_cards')
        if not self.table_cards:
            for player in self.active_players:
                for x in range(2):
                    if not self.deck.stack:
                        self.deck.populate()
                        self.deck.shuffle()
                    card = self.deck.stack.pop()
                    player.hand.append(card)
            for player in self.active_players:
                print(player, "hand ->", player.hand)

            for x in range(5):
                card = self.deck.stack.pop()
                self.table_cards.append(card)

            gui.create_cards(self, self.screen)
            print('Table cards', self.table_cards)

    def take_blinds(self):
        player_turn = self.dealer_seat + 1 if self.dealer_seat + 1 < len(self.seat) else 0
        self.current_player = self.seat[player_turn]
        if self.current_player in self.active_players:
            if self.current_player.bet != 0: raise ValueError('player.bet should be zero')
            if len(self.active_players) == 2:
                self.handle_big_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
            else:
                self.handle_small_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
                self.handle_big_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
        print('blinds taken')

    def handle_small_blind(self, current_player):
        if current_player.chips < self.sml_blind:
            current_player.bet = current_player.chips
            current_player.all_in = True
            self.highest_bet = current_player.bet
        else:
            current_player.bet = self.sml_blind
            current_player.chips -= current_player.bet


    def handle_big_blind(self, current_player):
        if current_player.chips < self.big_blind:
            current_player.bet = current_player.chips
            current_player.all_in = True
        else:
            current_player.bet = self.big_blind
            current_player.chips -= current_player.bet
        if current_player.bet > self.highest_bet:
            self.highest_bet = current_player.bet

    def add_flop_cards(self):
        for player in self.active_players:
            player.hand.append(self.table_cards[0])
            player.hand.append(self.table_cards[1])
            player.hand.append(self.table_cards[2])
        print('flop cards added')

    def update_highest_bet(self):
        big_bet = 0
        for player in self.active_players:
            if player.bet > big_bet:
                big_bet = player.bet
        self.highest_bet = big_bet

    def update_pot(self):
        for x in range(len(self.active_players)):
            self.pot.append(0)
        players_with_bets = [player for player in self.active_players if player.bet > 0]
        while players_with_bets:
            lowest_bet = min(player.bet for player in players_with_bets)

            for player in players_with_bets:
                if player.bet < lowest_bet:
                    lowest_bet = player.bet

            #add lowest bet to next pot eligibility
            for player in players_with_bets:
                self.pot[player.pot_eligibility] += lowest_bet
                player.bet -= lowest_bet

            #remove players with lowest bet
            new_list = [player for player in players_with_bets if player.bet != 0]
            players_with_bets = new_list

            #increment pot eligibility
            for player in players_with_bets:
                player.pot_eligibility += 1
        for player in self.active_players:
            if player.bet > 0: raise ValueError(f"{player}'s bet: {player.bet}(should be zero)")
        print('pot updated')

    def next_player(self, current_player):
        #returns the player whos turn is next
        next_player = None
        index = self.active_players.index(current_player)

        if self.active_players[-1] == self.active_players[index]:
            next_player = self.active_players[0]
        else:
            next_player = self.active_players[index + 1]
        print("player", current_player, "->", next_player)
        return next_player
    def equal_bets(self):
        #sent a list of players, returns True if all bets are equal to the highest bet
        print('equal bets? ->', self.active_players, "\nhighest bet ->", self.highest_bet)
        for player in self.active_players:
            if player.bet != self.highest_bet and player.all_in == False:
                return False
        print('equal bets!!!')
        return True
    def check_end_round(self) -> bool:
        if len(self.active_players) == 1:
            return True
        return False
    def end_round(self, winners:list):
        #recives a list of the winners of the round
        #splits the pot between the winners
        #gives money back to people with higher pot eligibility
        print('round over')
        ##splits the pot math
        eligibility = []
        for x in range(len(self.pot)):
            eligibility.append([])
            for player in self.seat:
                if player.pot_eligibility == x: eligibility[x].append(player)
            for player in winners:
                if player in eligibility[x]:
                    player.chips += self.pot[x] / len(winners)
                self.pot[x] -= self.pot[x] / len(winners)
            for player in eligibility[x]:
                player.chips += self.pot[x] / len(eligibility[x])
                self.pot[x] -= self.pot[x] / len(eligibility[x])
        #reset all game values and player values
        self.pot = [0]
        self.active_players = []
        self.round += 1
        self.bet_round = 0
        ##FIXME increase blinds when applicable
        self.dealer_seat += 1
        if self.dealer_seat == len(self.seat): self.dealer_seat = 0
        self.highest_bet = 0
        self.table_cards = []
        self.deck = Deck()
        for player in self.seat:
            player.hand = []
            player.bet = 0
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
    def check_end_game(self) -> bool:
        #checks all players chip count,
        x = 0
        for player in self.seat:
            if player.chips > 0:
                x += 1
        if x == 0:
            raise ValueError('at least one player must have chips')
        elif x == 1:
            return True
        else:
            return False
    def compare_hands(self, player:list)->list:
        #recieves a list of players
        #compares the hands of each of the players
        #returns list of player(s) with best hand
        #FIXME build this method
        return [player[0]]
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
        #print(f"Shuffled deck: {self.__repr__}")

    def populate(self):
        #populates all cards into the deck, only used in __init__
        for x in range(2, 15):
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
        self.width = self.front_image.get_width() * .8
        self.height = self.front_image.get_height() * .8
        self.front_image = pygame.transform.scale(self.front_image, (self.width, self.height))
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
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
        self.seat_number = -1

    def __str__(self):
        return f'Player {self.seat_number}'
    def __repr__(self):
        return f'Player[{self.seat_number}]'
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
    def _play(self, game:Game, input) -> bool :
        """
        Will control each turn that the player takes
        player input = {"fold":_fold, "check":_call, "call":_call, "bet":_bet}
        """
        move = {"fold":self._fold, "check":self._call, "call":self._call, "bet":self._bet}
        game.current_player = game.next_player(game.current_player)#switches player before they make a move because fold removes them from active players
        if not self.all_in:
            if input[0].lower() == 'bet':
                self._bet(game, input[1])
            else:
                move[input[0].lower()](game)


        return False
    def _get_input(self, game:Game) ->str:
        print('super class is being called')
        return 'fold'
    def get_moves(self, game:Game):
        ##takes in game state
        #returns a dictionary with the availble moves a player can take at the current moment
        moves = {"fold": True, "check": False, "call": False, "bet": False}
        if self.all_in:
            return {"fold": False, "check": False, "call": False, "bet": False}
        if game.highest_bet == self.bet:
            moves["check"] = True
        elif game.highest_bet > 0:
            moves["check"] = False
        else:
            moves["check"] = True

        if self.chips == 0 or game.highest_bet == 0 or self.bet == game.highest_bet:
            moves["call"] = False
        else:
            moves["call"] = True

        range = self.get_bet_range(game)
        if (self.bet + self.chips) < range[0]:
            moves["bet"] = False
        else:
            moves["bet"] = True

        return moves
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

        return True



    def get_bet_range(self, game:Game) -> (int,int):
        """
        Used to get the min and max values that the current player can bet
        if min_bet > max_bet, that means the current player cannot bet
        :param game:
        :return: (int, int)
        """
        highest_bet = 0
        highest_chip_count = 0
        second_highest_chip_count = 0
        for player in game.active_players:

            if player.chips >= highest_chip_count:
                second_highest_chip_count = highest_chip_count
                highest_chip_count = player.chips
            elif player.chips > second_highest_chip_count:
                second_highest_chip_count = player.chips
            if player.bet > highest_bet: highest_bet = player.bet
            game.highest_bet = highest_bet
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

        game.pot[self.pot_eligibility] += self.bet
        self.pot_eligibility = -1
        game.active_players.remove(self)
    def _call(self, game:Game):
        """
        player matches the highest bet on the table
        if highest bet is more than player has, player calls with all their chips and goes 'all-in'
        """
        if self.chips == 0:
            raise ValueError('player does not have any chips to call')
        elif (self.chips + self.bet) < game.highest_bet:
            self.bet += self.chips
            self.chips = 0
            self.all_in = True
        else:
            self.chips += self.bet
            self.bet = game.highest_bet
            self.chips -= self.bet
    def check_hand_rank(self, hand:list[Card]) -> None:
        """
        given a hand of cards, returns the type of hand
        sets the hand rank and best card
        """

class UserPlayer(Player):
    def __init__(self):
        super().__init__()
    def _play(self, game, input)->bool:
        """
        receives the input of the player, sends it to the super class
        """
        super()._play(game, input)
        return False

class AIPlayer(Player):
    def __init__(self):
        super().__init__()
    def _play(self, game)->bool:
        """
        controls the turn of a AI player
        """
        input = ("fold",0)
        super()._play(game, input)
        return False
'''
def main():
    deck = Deck()
    print(deck)
    print(len(deck.stack))


if __name__ == '__main__':
    main()
'''
