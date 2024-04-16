import pygame
import main
from game_model import *
from poker_gui import *
from main import *
from start_screen import *
from hand_rank_tests import *
import pytest
from unittest.mock import patch, MagicMock
import unittest



class TestMainFunctions(unittest.TestCase):
    def test_take_bets(self):
        # Create a mock game instance
        game = Game(num_User_players=4)
        player0 = UserPlayer()
        player1 = Player()
        player2 = Player()
        player3 = Player()
        game.active_players = [player0, player1, player2, player3]

        # Mock the input for each player's turn
        with patch('builtins.input', side_effect=['call', 'fold']):
            take_bets(game)

        # Check if the bet_round attribute has been incremented
        self.assertEqual(game.bet_round, 2)

    def test_get_player_input(self):
        # Create a mock game instance and player
        game = Game(num_User_players=4)
        player = UserPlayer()

        # Mock the input for the player's turn
        with patch('builtins.input', side_effect=[('bet', 50)]):
            move, bet_amount = get_player_input(game, player)

        # Check if the returned move and bet amount match the expected values
        self.assertEqual(move, 'bet')
        self.assertEqual(bet_amount, 50)

        
class TestSuit:

    #  Suit.HEARTS should return 'HEARTS'
    def test_suit_hearts(self):
        assert Suit.HEARTS.name == 'HEARTS'

    #  Suit.DIAMONDS should return 'DIAMONDS'
    def test_suit_diamonds(self):
        assert Suit.DIAMONDS.name == 'DIAMONDS'

    #  Suit(5) should raise ValueError
    def test_suit_value_error(self):
        with pytest.raises(ValueError):
            Suit(5)


class TestDeck:

    #  Deck is initialized with a full stack of 52 cards
    def test_deck_initialized_with_full_stack(self):
        deck = Deck()
        assert len(deck.stack) == 52

    #  Deck can be shuffled, changing the order of the cards
    def test_deck_can_be_shuffled(self):
        deck = Deck()
        original_stack = deck.stack.copy()
        deck.shuffle()
        assert deck.stack != original_stack

    #  Deck is initialized with no cards
    def test_deck_initialized_with_no_cards(self):
        deck = Deck()
        deck.stack = []
        assert len(deck.stack) == 0


class TestCard:

    #  Card object can be initialized with a value, suit, and image path
    def test_initialize_card_with_value_suit_and_image_path(self):
        card = Card(10, Suit.HEARTS, "Images/cardHearts10.png")
        assert card.value == 10
        assert card.suit == Suit.HEARTS
        assert card.front_image is not None
        assert card.back_image is not None

    #  Card object has a front image and a back image
    def test_card_has_front_and_back_image(self):
        card = Card(10, Suit.HEARTS, "Images/cardHearts10.png")
        assert card.front_image is not None
        assert card.back_image is not None


class TestPlayer:

    #  Player object is initialized with default values
    def test_player_initialized_with_default_values(self):
        player = Player()
        assert player.hand == []
        assert player.chips == 1000
        assert player.bet == 0
        assert player.pot_eligibility == 0
        assert player.winnings == 0
        assert not player.all_in
        assert player.seat_number == -1

    #  Player can set and get chips value
    def test_player_set_and_get_chips_value(self):
        player = Player()
        player.chips = 500
        assert player.chips == 500

    #  Player can get available moves
    def test_player_get_available_moves(self):
        player = Player()
        game = Game()
        game.highest_bet = 100
        player.bet = 50
        player.chips = 500
        moves = player.get_moves(game)
        assert moves == {"fold": True, "check": False, "call": True, "bet": True}
        player.bet = 100
        moves = player.get_moves(game)
        assert moves == {"fold": True, "check": True, "call": False, "bet": True}
        player.bet = 20
        player.chips = 20
        moves = player.get_moves(game)
        assert moves == {"fold": True, "check": False, "call": True, "bet": False}

    #  Player can call
    def test_player_call(self):
        player = Player()
        game = Game()
        game.highest_bet = 100
        player.bet = 50
        player.chips = 500
        player._call(game)
        assert player.bet == 100
        assert player.chips == 450

    #  Player cannot bet more than they have
    def test_player_cannot_bet_more_than_they_have(self):
        player = Player()
        game = Game()
        player.chips = 500
        with pytest.raises(ValueError):
            player._bet(game, 600)

    #  Player cannot bet less than 0
    def test_player_cannot_bet_less_than_zero(self):
        player = Player()
        game = Game()
        with pytest.raises(ValueError):
            player._bet(game, -50)

    #  Player cannot call if they do not have any chips
    def test_player_cannot_call_if_no_chips(self):
        player = Player()
        game = Game()
        player.chips = 0
        with pytest.raises(ValueError):
            player._call(game)


class TestUserPlayer:
    def test_instantiate_user_player(self):
        user_player = UserPlayer()
        assert isinstance(user_player, UserPlayer)

    def test_chips_property_negative_value(self):
        user_player = UserPlayer()
        with pytest.raises(ValueError):
            user_player.chips = -100


class TestAIPlayer:
    def test_instantiation(self):
        player = AIPlayer()
        assert isinstance(player, AIPlayer)

    def test_no_chips_left(self):
        player = AIPlayer()
        player.chips = 0
        assert player.chips == 0


class TestColor:

    #  The Color enum can be instantiated with valid RGB values
    def test_valid_rgb_values(self):
        color = Color.GREEN
        assert color.value == (0, 128, 0)

    #  The Color enum cannot be instantiated with invalid RGB values
    def test_invalid_rgb_values(self):
        with pytest.raises(ValueError):
            color = Color((256, 0, 0))

    #  The Color enum values cannot be modified
    def test_cannot_modify_values(self):
        with pytest.raises(AttributeError):
            Color.GREEN = (0, 255, 0)


class TestCreateCards:
    def test_display_correct_cards(self):
        game = Game()
        screen = pygame.Surface((800, 600))
        create_cards(game, screen)

    def test_empty_game_object(self):
        game = Game()
        screen = pygame.Surface((800, 600))
        create_cards(game, screen)
        # Assert that the function handles the case where the game object is empty
        assert game is None

    def test_empty_screen_object(self):
        game = Game()
        screen = None
        create_cards(game, screen)
        assert screen is None

class TestUpdate:
    def test_updates_screen(self):
        game = Game()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        update(game, screen, clock)

        assert pygame.display.get_surface().get_flags() & pygame.SRCALPHA


class TestRedrawScreen:
    def test_fill_screen_with_green_color(self):
        game = Game()
        screen = pygame.Surface((800, 600))
        clock = pygame.time.Clock()
        redraw_screen(game, screen, clock)

        assert screen.get_at((0, 0)) == Color.GREEN.value


class TestCreateButtons:

    #  Creates four buttons with correct positions and text
    def test_create_buttons_positions_and_text(self):
        game = Game()
        create_buttons(game)
        assert len(gui.buttons) == 4
        assert gui.buttons[0].x == 600
        assert gui.buttons[0].y == 550
        assert gui.buttons[0].width == 100
        assert gui.buttons[0].height == 50
        assert gui.buttons[0].text == "Fold"
        assert gui.buttons[1].x == 710
        assert gui.buttons[1].y == 550
        assert gui.buttons[1].width == 100
        assert gui.buttons[1].height == 50
        assert gui.buttons[1].text == "Check"
        assert gui.buttons[2].x == 600
        assert gui.buttons[2].y == 610
        assert gui.buttons[2].width == 100
        assert gui.buttons[2].height == 50
        assert gui.buttons[2].text == "Call"
        assert gui.buttons[3].x == 710
        assert gui.buttons[3].y == 610
        assert gui.buttons[3].width == 100
        assert gui.buttons[3].height == 50
        assert gui.buttons[3].text == "Bet"


class TestUpdateLabels:

    #  Resets all labels used in the game
    def test_reset_labels(self):
        game = Game()
        create_labels(game)

        # Modify the labels to have some text
        for label in labels_chip_count + labels_player_bet + label_pot + label_dealer + label_current_player_turn:
            label.text = "Test"

        # Call the function to reset the labels
        update_labels(game)

        # Check that all labels have been reset to empty text
        for label in labels_chip_count + labels_player_bet + label_pot + label_dealer + label_current_player_turn:
            assert label.text == ""


class TestButton:

    #  Button can be created with x, y, width, height, text, font_size and enabled parameters
    def test_create_button_with_parameters(self):
        button = Button(100, 200, 50, 30, "Test", 20, True)
        assert button.x == 100
        assert button.y == 200
        assert button.width == 50
        assert button.height == 30
        assert button.text == "Test"
        assert button.font_size == 20
        assert button.enabled == True

    #  Button can check if the mouse is hovering over it
    def test_check_hover(self):
        button = Button(100, 200, 50, 30, "Test", 20, True)
        assert button.check_hover((110, 210)) is True
        assert button.check_hover((90, 190)) is False

    #  Button can be created with no font_size parameter
    def test_create_button_without_font_size_parameter(self):
        button = Button(100, 200, 50, 30, "Test")
        assert button.font_size == 20

    #  Button can be created with no enabled parameter
    def test_create_button_without_enabled_parameter(self):
        button = Button(100, 200, 50, 30, "Test", 20)
        assert button.enabled is True

    #  Button can be created with text parameter as None
    def test_create_button_with_text_parameter_as_none(self):
        button = Button(100, 200, 50, 30, None, 20, True)
        assert button.text is None


class TestSlider:
    #  Slider can be drawn on the screen
    def test_draw_on_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        slider = Slider(100, 100, 200, 20, 0, 10, 1)
        slider.draw(screen)
        pygame.display.flip()
        pygame.quit()


class TestChip:

    #  can create a Chip object with a given position
    def test_create_chip_with_given_position(self):
        chip = Chip((100, 200))
        assert chip.rect.topleft == (100, 200)

    #  can change the size of a Chip object
    def test_change_chip_size(self):
        chip = Chip((100, 200))
        chip.change_size(0.5)
        assert chip.rect.width == chip.original_image.get_width() * 0.5
        assert chip.rect.height == chip.original_image.get_height() * 0.5

    #  can create a Chip object with a position of (0,0)
    def test_create_chip_with_position_zero_zero(self):
        chip = Chip((0, 0))
        assert chip.rect.topleft == (0, 0)

    #  can create a Chip object with a position of (screen_width, screen_height)
    def test_create_chip_with_position_screen_width_screen_height(self):
        screen_width = 800
        screen_height = 600
        chip = Chip((screen_width, screen_height))
        assert chip.rect.topleft == (screen_width, screen_height)

    #  can create a Chip object with a position of (screen_width+1, screen_height+1)
    def test_create_chip_with_position_screen_width_plus_one_screen_height_plus_one(self):
        screen_width = 800
        screen_height = 600
        chip = Chip((screen_width + 1, screen_height + 1))
        assert chip.rect.topleft == (screen_width + 1, screen_height + 1)

    #  can change the size of a Chip object to (0,0)
    def test_change_chip_size_to_zero(self):
        chip = Chip((100, 200))
        chip.change_size(0)
        assert chip.rect.width == 0
        assert chip.rect.height == 0


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_init(self):
        self.assertIsNotNone(self.game.deck)
        self.assertEqual(self.game.table_cards, [])
        self.game.seat = [UserPlayer(), UserPlayer(), UserPlayer()]
        self.assertEqual(len(self.game.seat), 3)
        self.assertTrue(all(isinstance(player, UserPlayer) for player in self.game.seat))

    def test_deal_initial_cards(self):
        # Mock the dependencies
        self.game.deck.populate = lambda: None
        self.game.deck.shuffle = lambda: None
        self.game.deck.stack = [MagicMock(front_image=pygame.Surface((1, 1))) for _ in range(52)]
        self.game.active_players = [UserPlayer() for _ in range(3)]

        self.game.deal_initial_cards()

    def test_start_round(self):
        screen_mock = MagicMock()
        self.game.seat = [MagicMock(chips=10) for _ in range(3)]
        self.game.start_round(screen_mock)
        self.assertEqual(self.game.round, 1)
        self.assertEqual(self.game.screen, screen_mock)
        self.assertEqual(len(self.game.active_players), 3)

    def test_take_blinds(self):
        self.game.seat = [MagicMock(chips=20) for _ in range(3)]
        self.game.take_blinds()
        self.assertFalse(all(player.bet in [10, 20] for player in self.game.seat))

    def test_handle_small_blind(self):
        player = MagicMock(chips=5)
        self.game.handle_small_blind(player)
        self.assertTrue(player.all_in)
        self.assertEqual(player.bet, 5)

    def test_handle_big_blind(self):
        player = MagicMock(chips=15)
        self.game.handle_big_blind(player)
        self.assertTrue(player.all_in)
        self.assertEqual(player.bet, 15)

    def test_add_flop_cards(self):
        self.game.active_players = [MagicMock(hand=[]) for _ in range(3)]
        self.game.table_cards = [MagicMock() for _ in range(5)]
        self.game.add_flop_cards()
        for player in self.game.active_players:
            self.assertEqual(len(player.hand), 3)

    def test_equal_bets(self):
        player1 = Player()
        player1.bet = 10
        player2 = Player()
        player2.bet = 10
        self.game.active_players = [player1, player2]
        self.game.highest_bet = 10

        result = self.game.equal_bets()

        self.assertTrue(result)

    def test_check_end_round(self):
        player = Player()  # Initialize your player here
        self.game.active_players = [player]

        result = self.game.check_end_round()

        self.assertTrue(result)


class Testmain(unittest.TestCase):

    def setUp(self):
        self.game = Game(num_User_players=3, num_AI_players=0)
        self.player = UserPlayer()

    def test_game_initialization(self):
        self.game.active_players = [UserPlayer(), UserPlayer(), UserPlayer()]
        self.assertEqual(len(self.game.active_players), 3)
        self.assertNotIn(AIPlayer, self.game.active_players)

    def test_player_initialization(self):
        self.assertEqual(self.player.chips, 1000)
        self.assertEqual(self.player.all_in, False)

    @patch('builtins.input', return_value='fold')
    def test_get_player_input_fold(self, input):
        move, bet_amount = get_player_input(self.game, self.player)
        self.assertEqual(move, 'fold')
        self.assertEqual(bet_amount, 0)

    @patch('builtins.input', return_value='check')
    def test_get_player_input_check(self, input):
        move, bet_amount = get_player_input(self.game, self.player)
        self.assertEqual(move, 'check')
        self.assertEqual(bet_amount, 0)



class TestTakeBets(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.user_player = UserPlayer()
        self.game.active_players = [self.user_player]
        self.game.current_player = self.user_player

    @patch('your_module.get_player_input', return_value=('check', 0))
    def test_take_bets_user_player(self, mock_get_player_input):
        result = take_bets(self.game)
        self.assertEqual(result, 0)
        mock_get_player_input.assert_called_once_with(self.game, self.user_player)


class TestStartScreen(unittest.TestCase):
    def setUp(self):
        self.start_screen = start_screen()

    def test_start_button(self):
        self.assertIsInstance(self.start_screen.start_button, pygame.Rect)
        self.assertEqual(self.start_screen.start_button.topleft, (300, 400))
        self.assertEqual(self.start_screen.start_button.size, (200, 50))

    def test_quit_button(self):
        self.assertIsInstance(self.start_screen.quit_button, pygame.Rect)
        self.assertEqual(self.start_screen.quit_button.topleft, (300, 500))
        self.assertEqual(self.start_screen.quit_button.size, (200, 50))

    def test_start_image(self):
        self.assertIsInstance(self.start_screen.start_image, pygame.Surface)


class TestGetPlayerInput(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player()
        self.game.screen = MagicMock()

    @patch('your_module.gui.Button')
    @patch('your_module.gui.Slider')
    def test_buttons_and_slider_creation(self, mock_slider, mock_button):
        with patch('your_module.pygame.event.get', return_value=[]):
            try:
                get_player_input(self.game, self.player)
            except:
                pass

        # Check that the buttons were created
        self.assertEqual(mock_button.call_count, 2)
        button_calls = [call.args for call in mock_button.call_args_list]
        self.assertIn((700, 460, 80, 30, "Submit Bet", 20, True), button_calls)
        self.assertIn((800, 460, 80, 30, "Cancel", 20, True), button_calls)

        # Check that the slider was created
        mock_slider.assert_called_once()


class TestHandRank(unittest.TestCase):


    def test_get_hand_rank_string(self):
        self.card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.card_suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        cards = [Card(self.card_values['2'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['3'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['4'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['5'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['6'], Suit.HEARTS, "Images/cardBack_red5.png")]
        self.assertEqual(get_hand_rank_string(cards), 'Straight6')

    def test_get_hand_rank(self):
        cards = [Card(self.card_values['2'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['3'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['4'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['5'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['6'], Suit.HEARTS, "Images/cardBack_red5.png")]
        self.assertEqual(get_hand_rank(cards), (5, cards))  # Straight

    def test_check_RoyalFlush(self):
        cards = [Card(self.card_values['10'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['J'], Suit.HEARTS,"Images/cardBack_red5.png"),
                 Card(self.card_values['Q'],  Suit.HEARTS,"Images/cardBack_red5.png"),
                 Card(self.card_values['K'],  Suit.HEARTS,"Images/cardBack_red5.png"),
                 Card(self.card_values['A'],  Suit.HEARTS,"Images/cardBack_red5.png")]
        self.assertEqual(check_RoyalFlush(cards), (True, cards))

    def test_check_StraightFlush(self):
        cards = [Card(self.card_values['2'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['3'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['4'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['5'], Suit.HEARTS, "Images/cardBack_red5.png"),
                 Card(self.card_values['6'],  Suit.HEARTS, "Images/cardBack_red5.png")]
        self.assertEqual(check_StraightFlush(cards), (False, cards))

    def test_four_of_a_kind(self):
        cards = [
            Card(8, Suit.HEARTS, "Images/cardBack_red5.png"),
            Card(8, Suit.DIAMONDS, "Images/cardBack_red5.png"),
            Card(8, Suit.CLUBS, "Images/cardBack_red5.png"),
            Card(8, Suit.SPADES, "Images/cardBack_red5.png"),
            Card(10, Suit.HEARTS, "Images/cardBack_red5.png")
        ]
        rank, _ = get_hand_rank(cards)
        self.assertEqual(rank, 2)


    def test_check_HighCard(self):
        # High Card: Ace high
        high_card = [
            Card(14, Suit.HEARTS, "Images/cardBack_red5.png"),
            Card(10, Suit.DIAMONDS, "Images/cardBack_red5.png"),
            Card(7, Suit.CLUBS, "Images/cardBack_red5.png"),
            Card(5, Suit.SPADES, "Images/cardBack_red5.png"),
            Card(2, Suit.HEARTS, "Images/cardBack_red5.png")
        ]
        self.assertTrue(check_HighCard(high_card)[0])


    def test_check_TwoPair(self):
        # Two Pair: Two Kings and Two Queens
        two_pair = [
            Card(13, Suit.HEARTS, "Images/cardBack_red5.png"),
            Card(13, Suit.DIAMONDS, "Images/cardBack_red5.png"),
            Card(12, Suit.CLUBS, "Images/cardBack_red5.png"),
            Card(12, Suit.SPADES, "Images/cardBack_red5.png"),
            Card(5, Suit.HEARTS, "Images/cardBack_red5.png")
        ]
        self.assertTrue(check_TwoPair(two_pair)[0])


    def test_check_ThreeOfAKind(self):
        # Three of a Kind: Three Jacks
        three_of_a_kind = [
            Card(11, Suit.HEARTS, "Images/cardBack_red5.png"),
            Card(11, Suit.DIAMONDS, "Images/cardBack_red5.png"),
            Card(11, Suit.CLUBS, "Images/cardBack_red5.png"),
            Card(7, Suit.SPADES, "Images/cardBack_red5.png"),
            Card(5, Suit.HEARTS, "Images/cardBack_red5.png")
        ]
        self.assertTrue(check_ThreeOfAKind(three_of_a_kind)[0])


if __name__ == '__main__':
    unittest.main()
