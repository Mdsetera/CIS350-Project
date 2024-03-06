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
        self.pot = []
        self.highest_bet = 0
        self.sml_blind = 10
        self.big_blind = 20

        self.dealer_seat = 0
        self.screen, self.clock = gui.init_pygame()

        for x in range(num_User_players):#add user players
            self.seat.append(UserPlayer())
        for x in range(num_AI_players):#add AI players
            self.seat.append(AIPlayer())
        for player in self.seat:
            player.seat_number = self.seat.index(player)

        ##everyone is now seated at the table


        self.round = 0 ##blind amount should increase every five rounds
        while not self.check_end_game():
            self.round += 1
            self.start_round(self.screen)
            self.deal_initial_cards()
            self.take_first_round_bets()



    def start_round(self, screen):
        ##deal the cards
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
        if not self.table_cards:
            for player in self.active_players:
                for x in range(2):
                    if not self.deck.stack:
                        self.deck.populate()
                        self.deck.shuffle()
                    card = self.deck.stack.pop()
                    player.hand.append(card)
            for player in self.active_players:
                print(player.hand)

            for x in range(5):
                card = self.deck.stack.pop()
                self.table_cards.append(card)

            gui.create_cards(self, self.screen)
            print(self.table_cards)

    def take_first_round_bets(self):
        player_turn = self.dealer_seat + 1 if self.dealer_seat + 1 < len(self.seat) else 0
        current_player = self.seat[player_turn]
        if current_player in self.active_players:
            if len(self.active_players) == 2:
                self.handle_big_blind(current_player)
            else:
                self.handle_small_blind(current_player)
                current_player = self.next_player(current_player)
                self.handle_big_blind(current_player)
        while (not self.equal_bets()):
                current_player._play(self) #FIX ME: need to recieve player input
        self.update_pot()


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


    def take_bets(self, show_cards_function, num_cards):
        self.show_table_cards(num_cards, show_cards_function, self.screen)
        self.update_pot()

    def show_table_cards(self, num_cards, show_cards_function, screen):
        #self.table_cards.extend(self.deck.stack[:num_cards])
        #print(f"After extending: {self.table_cards}")
        #self.deck.stack = self.deck.stack[num_cards:]
        show_cards_function(self, screen)

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

    def next_player(self, current_player):
        #returns the player whos turn is next
        index = self.active_players.index(current_player)
        if index == len(self.active_players) - 1:
            return self.active_players[0]
        return self.active_players[index + 1]

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
        print(f"Shuffled deck: {self.__repr__}")

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
        player input = {"fold":_fold, "check":_call, "call":_call, "bet":_bet}
        """
        #get the input

        return False

    def get_moves(self, game:Game):
        ##takes in game state
        #returns a dictionary with the availble moves a player can take at the current moment
        moves = {"fold": True, "check": False, "call": False, "bet": False}
        if self.all_in:
            return {"fold": False, "check": False, "call": False, "bet": False}
        if game.highest_bet > 0:
            moves["check"] = False
        else:
            moves["check"] = True

        if self.chips == 0:
            moves["call"] = False
        else:
            moves["call"] = True

        range = self.get_bet_range(game)
        if range[0] > range[1]:
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
    def _can_bet(self, game:Game)->bool:
        """FIXME"""
        return False

    def get_bet_range(self, game:Game) -> (int,int):
        """
        Used to get the min and max values that the current player can bet
        if min_bet > max_bet, that means the current player cannot bet
        :param game:
        :return: (int, int)
        """
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
    def _get_input(self, game):
        """
        controls the turn of a user
        """
        """FIXME
        show current players cards, hide everyone elses cards
        in poker_gui, we need a method that calls player.get_moves(),
        and returns the input players choses move
        player input = {0:_fold, 1:_check, 2:_call, 3:_bet}
        moves = {"fold": True, "check": False
        """
        input = 1
        return input

class AIPlayer(Player):
    def __init__(self):
        super().__init__()
    def _get_input(self, game):
        """
        controls the turn of a AI player
        """
        input = 0
'''
def main():
    deck = Deck()
    print(deck)
    print(len(deck.stack))


if __name__ == '__main__':
    main()
'''
