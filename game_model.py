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
    def __init__(self, num_User_players = 3):
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
        self.total_game_chips = 0

        for x in range(num_User_players):#add user players
            self.seat.append(UserPlayer())
        self.num_AI_players = 4 - num_User_players
        for x in range(self.num_AI_players):#add AI players
            self.seat.append(AIPlayer())
        for player in self.seat:
            player.seat_number = self.seat.index(player)
            self.total_game_chips += player.chips

        ##everyone is now seated at the table



    def start_round(self, screen):
        #iniitializes new round of play
        ##deal the cards
        self.round += 1
        self.screen = screen
        self.active_players = [player for player in self.seat if player.chips > 0]


    def deal_initial_cards(self):
        """
        deals two cards to each player
        and assigns five table cards to be shared
        amongst all players
        :return:
        """
        print('deal_initial_cards')
        if not self.table_cards:
            for player in self.seat:
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
        """
        blinds technically start the play
        big/little blinds must be taken in order for that person to play
        if there are only two players it only handles the big blind
        otherwise
        little blind is left of the dealer
        big blind is left of little blind
        if player does not have enough for the blind the remainder of their chips are taken and they go allin
        :return:
        """
        player_turn = self.dealer_seat + 1 if self.dealer_seat + 1 < len(self.seat) else 0
        if self.seat[player_turn] in self.active_players:
            self.current_player = self.seat[player_turn]
            if self.current_player.bet != 0: raise ValueError('player.bet should be zero')
            if len(self.active_players) == 2:
                self.handle_big_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
            else:
                self.handle_small_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
                self.handle_big_blind(self.current_player)
                self.current_player = self.next_player(self.current_player)
        else:
            player_turn = player_turn + 1 if player_turn + 1 < len(self.seat) else 0
        print('blinds taken')

    def handle_small_blind(self, current_player):
        #handles the small blind
        if current_player.chips < self.sml_blind:
            current_player.bet = current_player.chips
            current_player.all_in = True
            self.highest_bet = current_player.bet
        else:
            current_player.bet = self.sml_blind
            current_player.chips -= current_player.bet


    def handle_big_blind(self, current_player):
        #hanldes the big blind
        if current_player.chips < self.big_blind:
            current_player.bet = current_player.chips
            current_player.all_in = True
        else:
            current_player.bet = self.big_blind
            current_player.chips -= current_player.bet
        if current_player.bet > self.highest_bet:
            self.highest_bet = current_player.bet

    def add_flop_cards(self):
        """
        adds flop cards to each players hand
        :return:
        """
        for player in self.active_players:
            player.hand.append(self.table_cards[0])
            player.hand.append(self.table_cards[1])
            player.hand.append(self.table_cards[2])
        print('flop cards added')
    def add_turn_cards(self):
        #adds turn card to each players hand
        for player in self.active_players: player.hand.append(self.table_cards[3])
        print('turn card added')
    def add_river_cards(self):
        #adds river card to each players hand
        for player in self.active_players: player.hand.append(self.table_cards[-1])
        print('river card added')

    def update_highest_bet(self):
        """
        finds active player with the highest bet and updates game.highest_bet
        :return:
        """
        self.highest_bet = max([player.bet for player in self.active_players])
        print('highest bet ->', self.highest_bet)

    def update_pot(self):
        """
        adds every players bet to the pot
        assigns each player a pot eligibility
        based on how much they bet
        players are only eligible to recieve they amount that they bet from other players
        i,.e. player 1 bets 5 chips and is allin and player 2 and 3 bets 10 chips
        if player 1 wins the hand, player 1 recieves 5 from player 2 and 5 from player 3
        the remainder of player 2/3s chips are returned to them
        :return:
        """
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
    def previous_player(self, current_player):
        """
        receives a player and returns the player who will take their turn next
        :param current_player:
        :return:
        """
        #returns the player whos turn is next
        previous_player = None
        index = self.active_players.index(current_player)

        if self.active_players[0] == self.active_players[index]:
            previous_player = self.active_players[-1]
        else:
            previous_player = self.active_players[index - 1]
        #print("(previous player)", previous_player, "<-", current_player)
        return previous_player
    def next_player(self, current_player):
        """
        receives a player and returns the player who will take their turn next
        :param current_player:
        :return:
        """
        #returns the player whos turn is next
        next_player = None
        index = self.active_players.index(current_player)

        if self.active_players[-1] == self.active_players[index]:
            next_player = self.active_players[0]
        else:
            next_player = self.active_players[index + 1]
        print(current_player, "->", next_player,"(next_player)")
        return next_player
    def equal_bets(self):
        #sent a list of players, returns True if all bets are equal to the highest bet
        print('equal bets? ->', self.active_players)
        self.update_highest_bet()
        for player in self.active_players:
            if player.bet != self.highest_bet and player.all_in == False:
                return False
        print('equal bets!!!')
        return True
    def check_end_round(self) -> bool:
        #if there is only one player left return true
        if len(self.active_players) == 1:
            return True
        return False
    def end_round(self, winners:list):
        """
        receives the winner of the round and awards them chips based on their eligibilty
        if there are multiple winners the pot is split between them
        gives money back to players with higher eligibility
        resets and increments game state values
        resets player values
        :param winners:
        :return:
        """
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
                    player.chips += self.pot[x] // len(winners)
                self.pot[x] -= self.pot[x] // len(winners)
            for player in eligibility[x]:
                player.chips += self.pot[x] // len(eligibility[x])
                self.pot[x] -= self.pot[x] // len(eligibility[x])
        for player in self.seat:
            if isinstance(player, type(AIPlayer())):
                self.strategy_num = -1
            print(f'{player.__str__()} chips: {player.chips}', end=" ")
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
        total_table_chips = 0
        for player in self.seat:
            player.hand = []
            player.bet = 0
            player.fold = False
            if player.chips > 0: player.all_in = False
            total_table_chips += player.chips
        #if total_table_chips != self.total_game_chips: raise ValueError(f'Round: {self.round}, pot was not awarded correctly')
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
        #returns true if only one player has chips
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
    def compare_hands(self, players:list)->list:
        """
        recieves a list of players
        compares the hands of each of the players
        returns list of player(s) with best hand
        :param players: players whos hands to compare
        :return:
        """

        #FIXME build this method
        best_hand_rank = 100 #lowest number is best
        hand_rank = {}
        print('finding hand ranks')
        for player in players:
            hand_rank[player] = player.get_hand_rank()[0]
            if hand_rank[player] < best_hand_rank: best_hand_rank = hand_rank[player]
        compare = [player for player in hand_rank if hand_rank[player] == best_hand_rank]
        if len(compare) == 1:
            return [compare[0]]
        elif len(compare) == 0:
            raise ValueError('there must be a winner')
        else:
            print('comparing hands with the same rank')
            for x in range(len(compare[0].hand)):
                player_ranked = sorted(compare, key=lambda player: player.hand[x], reverse=True)
                best_card = player_ranked[0].hand[x]
                best_players = []
                for player in player_ranked:
                    if player.hand[x].value == best_card.value:
                        best_players.append(player)
                compare = best_players
                if len(compare) == 0:
                    raise ValueError('There must be at least one winner')
            return compare

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
        self.width = self.front_image.get_width() * .6
        self.height = self.front_image.get_height() * .6
        self.front_image = pygame.transform.scale(self.front_image, (self.width, self.height))
        self.back_image = pygame.transform.scale(self.back_image, (self.width, self.height))
        self.rect = self.front_image.get_rect()
        self.rect.topleft = (805, 0)
        self.width = self.rect.width
        self.height = self.rect.height


    def __repr__(self):
        return f'{self.value},{self.suit}'

    #these are used so you dont have to add .value to compare card values
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __eq__(self, other):
        return self.value == other.value

class Player:
    def __init__(self):
        self.hand = []
        self.chips = 100
        self.hand_rank = None
        self.bet = 0
        self.pot_eligibility = 0
        self.winnings = 0
        self.all_in = False
        self.seat_number = -1
        self.fold = False
        self.last_turn = None
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
        else:
            self._chips = num
    def _play(self, game:Game, input) -> bool :
        """
        Will control each turn that the player takes
        player input = {"fold":_fold, "check":_call, "call":_call, "bet":_bet}

        input:(function_name, amount)
        """
        move = {"fold":self._fold, "check":self._check, "call":self._call, "bet":self._bet}
        if not self.all_in and not self.fold: self.last_turn = input
        if not self.all_in and not self.fold:
            if input[0].lower() == 'bet':
                self._bet(game, input[1])
            else:
                move[input[0].lower()](game)
        return False
    def _get_input(self, game:Game) ->str:
        print('super class is being called')
        return ('fold', 0)
    def get_moves(self, game:Game):
        """
        takes in game state
        returns a dictionary with the availble moves a player can take at the current moment
        :param game: current game
        :return: moves dict
        """
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
        if (self.chips) < range[0] or range[0] > range[1]:
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
        elif (self.chips) < self.get_bet_range(game)[0]:#player cannot bet if they cannot match the minimum bet amount
            raise ValueError('player cannot meet minimum bet amount')
        else:
            self.bet += amount
            self.chips -= amount
            if self.chips == 0: self.all_in = True
        return True

    def get_bet_range(self, game:Game) -> (int,int):
        """
        Used to get the min and max values that the current player can bet
        if min_bet > max_bet, that means the current player cannot bet
        :param game:
        :return: (min bet, max bet)
        """
        bets = [player.bet for player in game.active_players]
        #find each players total amount of chips, that being the bet + remaining chips. not including the current player (self)
        total_chips = [player.bet + player.chips for player in game.active_players if not player is self]
        highest_bet = max(bets)

        # amount neded to match the highest bet
        min_bet = (highest_bet - self.bet) + 1

        # max_bet is calculated as the maximum of total chips among other players
        # minus the current player's bet, or the remaining chips of the current player (self.chips), whichever is smaller.
        max_bet = max(total_chips) - self.bet if max(total_chips) - self.bet < self.chips else self.chips

        return min_bet, max_bet

    def get_hand_rank(self) -> (int, [Card]):
        """
        resets player hand to new order
        :return: (hand rank, player hand in new order)
        """
        if self.hand == []:
            return (-1, self.hand)
        import hand_rank_tests as rank
        rank, self.hand = rank.get_hand_rank(self.hand)
        return rank, self.hand
    def get_hand_rank_str(self) ->str:
        """
        :return: hand rank as a string
        """
        if self.hand == []:
            return 'No cards'
        import hand_rank_tests as rank
        return rank.get_hand_rank_string(self.hand)
    def _check(self, game:Game):
        #check does nothing lol
        pass
    def _fold(self, game:Game):
        """
        player ends involvement in the round and forfeits eligibility to the pot
        """

        game.pot[self.pot_eligibility] += self.bet
        self.pot_eligibility = -1
        self.fold = True
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
            if self.chips == 0: self.all_in = True

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
        self.strategy_num = -1
    def _play(self, game, input = ('fold', 0)):
        """
        will control the turn of a AI player
        """

        #['Royal Flush-0', 'StraightFlush-1', 'FourOfAKind-2', 'FullHouse-3', 'Flush-4']
        #['Straight-5', 'ThreeOfAKind-6', 'TwoPair-7', 'Pair-8', 'High-9'])

        num_strategies = 4 #when creating a new strategy, this number must be incremented manually

        if self.strategy_num == -1:
            self.strategy_num = random.randint(0, num_strategies-1)
        input = self.get_strategy(game)
        super()._play(game, input)#AI player
    def get_strategy(self, game) -> (str,int):
        rank, self.hand = self.get_hand_rank()
        moves = self.get_moves(game)
        #bet rounds start at 1, every round, and increments 1 everytime a new round-of-bets starts
        if self.strategy_num == -1: return ('fold', 0)
        #strategy 0 - conservative
        if self.strategy_num == 0:
            last_turn = game.previous_player(self).last_turn #last turn of the previous player
            if rank == 9 and game.bet_round > 1:
                if self.hand[0].value >= 12:
                    return ('call', 0)
                else:
                    return ('fold', 0)
            elif rank == 8: #pair
                if last_turn[0] == 'bet':
                    if last_turn[1] > self.bet + (self.chips * 100) // 20:
                        return ('fold', 0)
                    else:
                        return ('call', 0)
                elif last_turn[0] == 'call':
                    if game.highest_bet > self.bet + (self.chips * 100) // 20:
                        return ('fold', 0)
                    else:
                        return ('call', 0)
                elif last_turn[0] == 'check':
                    if moves['check']: return ('check', 0)
            elif game.highest_bet > self.bet + (self.chips * 100) // 50:
                return ('fold',0)
            elif rank < 8:
                if moves['call']: return ('call', 0)
            else:
                return ('fold', 0)

        #strategy 1 - going shot for shot
        elif self.strategy_num == 1:
            if moves['check'] == True:#if bot can check it will
                return ('check', 0)
            elif moves['call'] == True:#then if it can call it will
                return ('call', 0)
            else:
                return ('fold', 0)

        #strategy 2 - bluffing with random bets
        elif self.strategy_num == 2:
            if moves['bet'] == True:
                range = self.get_bet_range(game)
                random_bet = random.randint(range[0], range[1])
                print(f'Chips: {self.chips} Bet: {self.bet} Bet-Range: {range} Trying to bet -> {random_bet}')
                return ('bet', random_bet)
            elif moves['call'] == True:
                return ('call', 0)
            elif moves['check'] == True:  # if bot can check it will
                return ('check', 0)
            else:
                return ('fold', 0)
        #strategy 3 - check raise
        elif self.strategy_num == 3: #check raise
            if moves['check'] == True:
                return ('check', 0)
            elif moves['bet'] is True and self.last_turn != None and self.last_turn[0] != 'bet':
                range = self.get_bet_range(game)
                bet_num = (range[1] + range[0])//2
                print(f'Chips: {self.chips} Bet: {self.bet} Bet-Range: {range} Trying to bet -> {bet_num}')
                return ('bet', bet_num)
            elif moves['call'] == True: return ('call', 0)
            else:
                return ('fold', 0)
        else:
            raise ValueError(f'invalid strategy_num')
        raise ValueError(f'Strategy {self.strategy_num} not working')
'''
def main():
    deck = Deck()
    print(deck)
    print(len(deck.stack))


if __name__ == '__main__':
    main()
'''
