from game_model import *
from poker_gui import *
from main import *
from start_screen import *
import pytest


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

    #  can instantiate UserPlayer object
    def test_instantiate_user_player(self):
        user_player = UserPlayer()
        assert isinstance(user_player, UserPlayer)

    #  chips property raises ValueError if set to negative number
    def test_chips_property_negative_value(self):
        user_player = UserPlayer()
        with pytest.raises(ValueError):
            user_player.chips = -100


class TestAIPlayer:

    #  AIPlayer can be instantiated without errors
    def test_instantiation(self):
        player = AIPlayer()
        assert isinstance(player, AIPlayer)

    #  AIPlayer can handle not having any chips left
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

    #  The function displays the correct cards for each player and the table depending on the current round of betting.
    def test_display_correct_cards(self):
        game = Game()
        screen = pygame.Surface((800, 600))
        create_cards(game, screen)
        # Assert that the correct cards are displayed for each player and the table
        # based on the current round of betting

    #  The function handles the case where the game object is empty.
    def test_empty_game_object(self):
        game = Game()
        screen = pygame.Surface((800, 600))
        create_cards(game, screen)
        # Assert that the function handles the case where the game object is empty

    #  The function handles the case where the screen object is empty.
    def test_empty_screen_object(self):
        game = Game()
        screen = None
        create_cards(game, screen)
        # Assert that the function handles the case where the screen object is empty


class TestUpdate:

    #  updates the screen based on the current game state
    def test_updates_screen(self):
        game = Game()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        update(game, screen, clock)

        # Assert that the screen has been updated
        assert pygame.display.get_surface().get_flags() & pygame.SRCALPHA


class TestRedrawScreen:

    #  fills the screen with green color
    def test_fill_screen_with_green_color(self):
        # Arrange
        game = Game()
        screen = pygame.Surface((800, 600))
        clock = pygame.time.Clock()

        # Act
        redraw_screen(game, screen, clock)

        # Assert
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
        assert button.check_hover((110, 210)) == True
        assert button.check_hover((90, 190)) == False

    #  Button can be created with no font_size parameter
    def test_create_button_without_font_size_parameter(self):
        button = Button(100, 200, 50, 30, "Test")
        assert button.font_size == 20

    #  Button can be created with no enabled parameter
    def test_create_button_without_enabled_parameter(self):
        button = Button(100, 200, 50, 30, "Test", 20)
        assert button.enabled == True

    #  Button can be created with text parameter as None
    def test_create_button_with_text_parameter_as_none(self):
        button = Button(100, 200, 50, 30, None, 20, True)
        assert button.text == None


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

