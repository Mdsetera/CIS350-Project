import os.path

import pygame
from enum import Enum

window_start_Width = 805
window_start_Height = 685

buttons = []
labels_chip_count = []
labels_player_bet = []
label_pot = []
label_dealer = []
label_current_player_turn = []
label_player_hands = []
bet_chips = []
class Color(Enum):
    """
    holds (R,G,B) values for different colors
    """
    GREEN = (0, 128, 0)
    BLUE = (0,0,255)
    LGREEN = (0, 255, 0)
    RED = (255,0,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
##method()
def init_pygame():
    """
    initializes the game window
    :return:
    """
    pygame.init()
    global window_start_Width, window_start_Height
    screen = pygame.display.set_mode((window_start_Width, window_start_Height), pygame.RESIZABLE)
    pygame.display.set_caption("Texas Hold'Em!")
    clock = pygame.time.Clock()
    #icon_image = pygame.image.load("images\icon.png")
    #pygame.display.set_icon(icon_image)

    return screen, clock



def show_flop(game, screen):
    """
    Draws the first three shared cards of the round (the flop) on the screen and animates their movement.
    :param game: The game state object containing information about the game.
    :param screen: The Pygame screen object where the cards will be displayed.
    """
    # Define the target positions for the flop cards
    flop_positions = [(250, 225), (310, 225), (370, 225)]

    # Iterate through the first three flop cards
    for index, card in enumerate(game.table_cards[:3]):
        # Set the initial position of each card to an off-screen starting point (805, 0)
        initial_position = (805, 0)
        card.rect.topleft = initial_position

        # Calculate the target position for the current card
        target_position = flop_positions[index]

        # Animate the card moving from the initial position to the target position
        move_card(game, screen, card, target_position, speed=10)
        # Redraw all existing cards (player cards, other table cards) on the screen to maintain the screen state
        for player in game.seat:
            for player_card in player.hand:
                screen.blit(player_card.front_image, player_card.rect)

        for j in range(index + 1):
            current_card = game.table_cards[j]
            screen.blit(current_card.front_image, current_card.rect)


        # Update the display to reflect the current state of the screen
        pygame.display.update()
        # Add a delay between animations for smoother animation
        pygame.time.delay(300)
    # Final update to the display
    update_labels(game)
    create_buttons(game)
    pygame.display.update()

def show_turn(game, screen):
    """
    draws the 4th shared card of the round on the screen
    :param game:
    :param screen:
    :return:
    """
    turn_card = game.table_cards[3]
    initial_position = (805, 0)
    turn_card.rect.topleft = initial_position
    target_position = (430, 225)

    move_card(game, screen, turn_card, target_position, speed=10)
    for player in game.seat:
        for player_card in player.hand:
            screen.blit(player_card.front_image, player_card.rect)

    screen.blit(turn_card.front_image, turn_card.rect)

    pygame.display.update()
    pygame.time.delay(300)
    pygame.display.update()


def show_river(game, screen):
    """
    draws the 5th shared card of the round on the screen
    :param game:
    :param screen:
    :return:
    """
    river_card = game.table_cards[4]
    initial_position = (805, 0)
    river_card.rect.topleft = initial_position
    target_position = (490, 225)

    move_card(game, screen, river_card, target_position, speed=10)
    for player in game.seat:
        for player_card in player.hand:
            screen.blit(player_card.front_image, player_card.rect)

    screen.blit(river_card.front_image, river_card.rect)

    pygame.display.update()
    pygame.time.delay(300)
    pygame.display.update()

#Card Sizes & Position


def create_cards(game, screen):
    """
    Creates and draws all cards for all players on the screen.
    """
    if game.bet_round >= 2:
        show_flop(game, screen)
    if game.bet_round >= 3:
        show_turn(game, screen)
    if game.bet_round >= 4:
        show_river(game, screen)

    card_locations = [(350, 445), (380, 445), (15, 220), (15, 250), (350, 15), (350, 15), (675, 220), (675, 250)]
    # Iterate through each player in the game
    for player_index, player in enumerate(game.seat):
        for card_index, card in enumerate(player.hand):
            # Ensure we don't go out of range in card_locations
            if player_index * 2 + card_index < len(card_locations):
                # Set the initial position of each card in the upper right corner at (805, 0)
                initial_position = (805, 0)
                card.rect.topleft = initial_position
                # Determine target positions for each card
                target_position = card_locations[player_index * 2 + card_index]

                # Handle card rotation based on player position
                if player == game.seat[1] or player == game.seat[3]:
                    card.front_image = pygame.transform.rotate(card.back_image, 90)
                    # Adjust the card's rect for the rotated image
                    card.rect = card.front_image.get_rect(center=card.rect.center)
                if player == game.seat[2]:
                    card.front_image = card.back_image

                # Move the card to its target position
                move_card(game, screen, card, target_position, speed=20)

    # After all cards have been moved, draw all cards on the screen
    for player in game.seat:
        for card in player.hand:
            # Display the card image at its position
            screen.blit(card.front_image, card.rect)

    # Update buttons and labels once all cards are in position
    create_buttons(game)
    create_labels(game)
    # Update the display
    pygame.display.flip()


def move_card(game, screen, card, target_position, speed=10):
    # Initialize the clock for controlling frame rate
    clock = pygame.time.Clock()

    # Calculate initial differences and distance between current and target positions
    x_difference = target_position[0] - card.rect.x
    y_difference = target_position[1] - card.rect.y
    distance = (x_difference ** 2 + y_difference ** 2) ** 0.5

    # Calculate initial offsets for smooth movement
    ratio = speed / distance
    offset_x = x_difference * ratio
    offset_y = y_difference * ratio

    # Initial setup of labels and buttons
    create_labels(game)
    create_buttons(game)

    # Initialize previous position to card's initial position
    previous_position = card.rect.copy()

    # Run the animation loop
    while distance > speed:
        # Update card position incrementally
        card.rect.x += offset_x
        card.rect.y += offset_y

        # Calculate remaining distance
        x_difference = target_position[0] - card.rect.x
        y_difference = target_position[1] - card.rect.y
        distance = (x_difference ** 2 + y_difference ** 2) ** 0.5

        # Calculate new offsets for the next iteration
        ratio = speed / distance if distance != 0 else 0
        offset_x = x_difference * ratio
        offset_y = y_difference * ratio

        # Clear only the area of the previous card position
        pygame.draw.rect(screen, Color.GREEN.value, previous_position)

        # Update the previous position to the current position
        previous_position = card.rect.copy()

        # Draw player hands
        for player in game.seat:
            for player_card in player.hand:
                screen.blit(player_card.front_image, player_card.rect)

        # Draw all table cards
        for table_card in game.table_cards:
            screen.blit(table_card.front_image, table_card.rect)

        # Draw the moving card in its new position
        screen.blit(card.front_image, card.rect)

        # Update the display
        pygame.display.update()
        update_labels(game)
        # Control the frame rate for smooth animation
        clock.tick(60)

    # Once the card reaches the target position, set the final position
    card.rect.topleft = target_position

    # Final redraw after animation completion
    screen.fill(Color.GREEN.value)  # Clear the screen
    # Redraw all player hands
    for player in game.seat:
        for player_card in player.hand:
            screen.blit(player_card.front_image, player_card.rect)

    # Redraw all table cards
    for table_card in game.table_cards:
        screen.blit(table_card.front_image, table_card.rect)

    # Draw labels and buttons again at the end of the function
    update_labels(game)
    create_buttons(game)

    # Update the display to reflect the final state
    pygame.display.update()


def change_dimensions(game, new_Width, new_Height):
    """
    receives a new width and height and redraws the window and screen with the new dimensions
    :param game:
    :param new_Width:
    :param new_Height:
    :return:
    """
    global window_start_Width, window_start_Height

    x_scale = new_Width / window_start_Width
    y_scale = new_Height / window_start_Height

    window_start_Width = new_Width
    window_start_Height = new_Height

    for player in game.active_players:
        for card in player.hand:
            card.rect.width = int(card.rect.width * x_scale)
            card.rect.height = int(card.rect.height * y_scale)

            card.front_image = pygame.transform.scale(card.front_image, (card.rect.width, card.rect.height))
            card.back_image = pygame.transform.scale(card.back_image, (card.rect.width, card.rect.height))
        #raise NotImplementedError('need to create way to change button dimensions')
        ##currently buttons are made in main.get_user_input()
        #list of buttons updated every time a new button is created
    pygame.display.flip()


def update(game, screen, clock):
    """
    function used to redraw all the current shared cards
    :param game:
    :param screen:
    :param clock:
    :return:
    """
    if game.bet_round == 2:
        show_flop(game, screen)
    elif game.bet_round == 3:
        show_turn(game, screen)
    elif game.bet_round == 4:
        show_river(game, screen)

    pygame.display.flip()


def redraw_screen(game, screen, clock):
    """
    redraws the screen
    :param game:
    :param screen:
    :param clock:
    :return:
    """
    screen.fill(Color.GREEN.value)
    update(game, screen, clock)
    pygame.display.flip()


def create_buttons(game):
    """
    creates and draws all main 4 buttons onto the screen
    :param game:
    :return:
    """
    fold_button = Button(365, 630, 100, 50, "Fold", 30, False)
    check_button = Button(475, 630, 100, 50, "Check", 30, False)
    call_button = Button(585, 630, 100, 50, "Call", 30, False)
    bet_button = Button(695, 630, 100, 50, "Bet", 30, False)
    fold_button.draw(game.screen)
    check_button.draw(game.screen)
    call_button.draw(game.screen)
    bet_button.draw(game.screen)
    pygame.display.flip()


def enable_buttons(game, player):
    """
    recieves a player, and enables/disables buttons
    based on what moves the player is allowed to make
    :param game:
    :param player:
    :return:
    """
    moves = player.get_moves(game)
    for button in buttons:
        button.enabled = False
        if moves['fold'] and button.text == 'Fold':
            button.enabled = True
        elif moves['check'] and button.text == 'Check':
            button.enabled = True
        elif moves['call'] and button.text == 'Call':
            button.enabled = True
        elif moves['bet'] and button.text == 'Bet':
            button.enabled = True
        button.draw(game.screen)
    pygame.display.flip()


def create_labels(game):
    """
    creates and draws all labels
    that the user will use to keep track of the game state
    :param game:
    :return:
    """
    import hand_rank_tests as rank
    global labels_chip_count,labels_player_bet, label_pot, label_dealer, label_current_player_turn, bet_chips
    bet_chips = []
    labels_chip_count = []
    labels_player_bet = []
    label_pot = []
    label_dealer = []
    label_current_player_turn = []

    l_dealer = Label(f"Dealer: Player {game.dealer_seat}", 40, (0, 0, 0), (5, 5))
    l_dealer.draw(game.screen)
    label_dealer.append(l_dealer)

    #Player 0 labels
    label0_text = f'{int(game.seat[0].chips)}'
    label0_bet_text = f'{int(game.seat[0].bet)}'
    label0_hand_text = game.seat[0].get_hand_rank_str()
    player0_balance = Label(label0_text, 25, Color.BLACK, (380, 564))
    player0_bet = Label(label0_bet_text, 25, Color.WHITE, (380, 420), visible=game.seat[0].bet>0)
    player0_hand = Label(label0_hand_text, 25, Color.BLACK, (340, 600))
    chip1_player0 = Chip((350, 563))
    chip1_player0.change_size(.3)
    bet_chips.append(Chip((350, 419), visible=game.seat[0].bet>0))
    bet_chips[0].change_size(.3)
    label_player_hands.append(player0_hand)
    labels_chip_count.append(player0_balance)
    labels_player_bet.append(player0_bet)

    #Player 1 labels
    label1_text = f'{int(game.seat[1].chips)}'
    label1_bet_text = f'{int(game.seat[1].bet)}'
    label1_hand_text = game.seat[1].get_hand_rank_str()
    player1_balance = Label(label1_text, 25, Color.BLACK, (45, 340))
    chip1_player1 = Chip((15, 339))
    chip1_player1.change_size(.3)
    bet_chips.append(Chip((120, 340), visible=game.seat[1].bet>0))
    bet_chips[1].change_size(.3)
    player1_bet = Label(label1_bet_text, 25, Color.WHITE, (145, 340), visible=game.seat[1].bet>0)
    player1_hand = Label(label1_hand_text, 25, Color.LGREEN, (80, 370))
    label_player_hands.append(player1_hand)
    labels_chip_count.append(player1_balance)
    labels_player_bet.append(player1_bet)

    #Player 2 labels
    label2_text = f'{int(game.seat[2].chips)}'
    label2_bet_text = f'{int(game.seat[2].bet)}'
    label2_hand_text = game.seat[2].get_hand_rank_str()
    player2_balance = Label(label2_text, 25, Color.BLACK, (380, 135))
    chip1_player2 = Chip((350, 134))
    chip1_player2.change_size(.3)
    bet_chips.append(Chip((350, 160), visible=game.seat[2].bet>0))
    bet_chips[2].change_size(.3)
    player2_bet = Label(label2_bet_text, 25, Color.WHITE, (380, 161), visible=game.seat[2].bet>0)
    player2_hand = Label(label2_hand_text, 25, Color.LGREEN, (895, 480))
    label_player_hands.append(player2_hand)
    labels_chip_count.append(player2_balance)
    labels_player_bet.append(player2_bet)


    #Player 3 labels
    label3_text = f'{int(game.seat[3].chips)}'
    label3_bet_text = f'{int(game.seat[3].bet)}'
    label3_hand_text = game.seat[2].get_hand_rank_str()
    player3_balance = Label(label3_text, 25, Color.BLACK, (700, 340))
    chip1_player3 = Chip((675, 339))
    chip1_player3.change_size(.3)
    bet_chips.append(Chip((620, 360), visible=game.seat[3].bet>0))
    bet_chips[3].change_size(.3)
    player3_bet = Label(label3_bet_text, 25, Color.WHITE, (650, 361), visible=game.seat[3].bet>0)
    player3_hand = Label(label3_hand_text, 25, Color.LGREEN, (895, 480))
    label_player_hands.append(player3_hand)
    labels_chip_count.append(player3_balance)
    labels_player_bet.append(player3_bet)


    player0_balance.draw(game.screen)
    player0_bet.draw(game.screen)
    #player0_hand.draw(game.screen)
    player1_balance.draw(game.screen)
    player1_bet.draw(game.screen)
    #player1_hand.draw(game.screen)
    player2_balance.draw(game.screen)
    player2_bet.draw(game.screen)
    #player2_hand.draw(game.screen)
    player3_balance.draw(game.screen)
    player3_bet.draw(game.screen)



    chip1_player0.draw(game.screen)
    chip1_player1.draw(game.screen)
    chip1_player2.draw(game.screen)
    chip1_player3.draw(game.screen)




    #pot label
    total_pot = 0
    for pot in game.pot:
        total_pot += pot
    label_pot.append(Label(f"Pot: 0", 40, Color.RED, (385, 352), visible=total_pot>0))
    label_pot[0].text = f'{total_pot}'
    label_pot[0].draw(game.screen)
    bet_chips.append(Chip((350, 350), visible=label_pot[0].visible))
    bet_chips[-1].change_size(.4)
    bet_chips.append(Chip((460, 350), visible=label_pot[0].visible))
    bet_chips[-1].change_size(.4)
    for chip in bet_chips: chip.draw(game.screen)

    label_current_player_turn.append(Label(f'{game.current_player}\'s turn', 40, Color.BLACK, (5, 40)))
    label_current_player_turn[0].draw(game.screen)

    #fold lables
    label_fold = []
    #print("Players in seats ->", game.seat)
    #print(f"[{game.seat[0].fold},{game.seat[1].fold},{game.seat[2].fold}]")
    label_fold.append(Label('FOLD', 60, Color.BLACK, (350, 445+20), visible = game.seat[0].fold))
    label_fold[0].rotate(20)
    label_fold[0].draw(game.screen)

    label_fold.append(Label('FOLD', 60, Color.BLACK, (15, 220+20), visible = game.seat[1].fold))
    label_fold[1].rotate(20)
    label_fold[1].draw(game.screen)

    label_fold.append(Label('FOLD', 60, Color.BLACK, (350, 15+20), visible = game.seat[2].fold))
    label_fold[2].rotate(20)
    label_fold[2].draw(game.screen)

    label_fold.append(Label('FOLD', 60, Color.BLACK, (675, 220+20), visible = game.seat[3].fold))
    label_fold[3].rotate(20)
    label_fold[3].draw(game.screen)

    #all in lables
    label_player_all_in = []
    label_player_all_in.append(Label('ALL IN', 50, Color.BLACK, (350, 445+20), visible = game.seat[0].all_in))
    label_player_all_in[0].rotate(20)
    label_player_all_in[0].draw(game.screen)

    label_player_all_in.append(Label('ALL IN', 50, Color.BLACK, (15, 220+20), visible = game.seat[1].all_in))
    label_player_all_in[1].rotate(20)
    label_player_all_in[1].draw(game.screen)

    label_player_all_in.append(Label('ALL IN', 50, Color.BLACK, (350, 15+20), visible = game.seat[2].all_in))
    label_player_all_in[2].rotate(20)
    label_player_all_in[2].draw(game.screen)

    label_player_all_in.append(Label('ALL IN', 50, Color.BLACK, (350, 15+20), visible = game.seat[2].all_in))
    label_player_all_in[3].rotate(20)
    label_player_all_in[3].draw(game.screen)




    pygame.display.flip()


def update_labels(game):
    """
    takes all the labels and fills them with the background color (Green)
    so that they can be redrawn with their new text values
    :param game:
    :return:
    """
    #reset all labels used in the game
    #erase label text by redrawing
    for label in labels_chip_count + labels_player_bet + label_pot + label_dealer + label_current_player_turn + label_player_hands + bet_chips:
        new = pygame.Surface(label.rect.size)
        new.fill(Color.GREEN.value)
        game.screen.blit(new, label.rect.topleft)
    #set labels to new text
    create_labels(game)


    pygame.display.flip()

def print_winner(screen, winner):
    """
    current way to end the game
    just makes a big label
    declaring who won that game
    :param screen:
    :param winner:
    :return:
    """
    winner_label = Label(f'{winner.__str__()} is the winner!!!', 100, Color.WHITE, (100,330))
    winner_label.draw(screen)
    pygame.display.flip()
class Button:
    def __init__(self, x, y, width, height, text, font_size=20, enabled=True, visible=True):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.enabled = enabled
        self.font = pygame.font.Font(None, self.font_size)
        self._visible = visible
        buttons.append(self)
    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if isinstance(value, bool):
            if value:
                self._visible = value
    def remove(self, screen):
        """
        fills the button surface with the color green
        :param screen:
        :return:
        """
        new = pygame.Surface((self.width, self.height))
        new.fill(Color.GREEN.value)
        screen.blit(new, (self.x, self.y))
    def draw(self, screen):
        if self.visible:
            if self.enabled:
                button_color = (0, 0, 255)
                text_color = (255, 255, 255)
            else:
                button_color = (128, 128, 128)
                text_color = (0, 0, 0)

            pygame.draw.rect(screen, button_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
            button_text = self.font.render(self.text, True, text_color)
            text_rect = button_text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(button_text, text_rect)

    def check_hover(self, mouse_pos):
        #checks is mouse position is hovering over the button
        #returns true if it is
        #mouse_pos = pygame.mouse.get_pos()
        x_Overbutton = self.x <= mouse_pos[0] <= self.x + self.width
        y_Overbutton = self.y <= mouse_pos[1] <= self.y + self.height
        #print(f'Hover check for button\'{self.text}\': {x_Overbutton and y_Overbutton}')
        return x_Overbutton and y_Overbutton

    def check_click(self, mouse_pos, events):
        #checks if button was clicked
        #returns true if it was
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_hover(mouse_pos):
                    print(f'clicked \'{self.text}\' button')
                    return True
        return False


class Slider:
    def __init__(self, x, y, width, height, minimum, maximum, step, visible=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.minimum = minimum
        self.maximum = maximum
        self.width = ((maximum - minimum) / step) * 3
        self.x -= self.width
        self.step = step
        self.value = minimum
        self.slider_rect = pygame.Rect(self.x, self.y + height // 3, self.width, height // 3)
        self.pointer_rect = pygame.Rect(self.x+self.width, y, 20, height)
        self.dragging = False


    def draw(self, screen):
        #draws slider bar
        pygame.draw.rect(screen, (200, 200, 200), self.slider_rect)
        #draw slider pointer
        pygame.draw.rect(screen, (0, 0, 0), self.pointer_rect)

        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + self.height + 5, self.width, 15))
        #draw value
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.value), True, (0, 0, 0))

        screen.blit(text, (self.x + self.width // 2, self.y + self.height + 5))

    def handle_click(self, mouse_pos):
        #checks if slider pointer wsa clicked
        mouse_x, mouse_y = mouse_pos
        if self.pointer_rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True

    def handle_drag(self, mouse_pos):
        #modifies the value of the slider depending on where the slider is dragged
        if self.dragging:
            mouse_x, mouse_y = mouse_pos

            pointer_x = max(self.x, min(mouse_x - self.pointer_rect.width // 2, self.x + self.width))
            self.pointer_rect.x = pointer_x

            # Calculate the position of the pointer relative to the slider's width
            relative_pos = 1 - ((pointer_x - self.x) / self.width)
            # Update the value accordingly
            self.value = int(relative_pos * (self.maximum - self.minimum) / self.step) * self.step + self.minimum

    def handle_release(self):
        #stops drag when you stop clicking the slider
        self.dragging = False

    def move_slider(self, mouse_pos):
        #moves the slider pointer as the user draggs it
        self.pointer_rect.centerx = mouse_pos[0]

    def remove(self, screen):
        """
        fills the button surface with the color green
        :param screen:
        :return:
        """
        new = pygame.Surface((self.width, self.height))
        new.fill(Color.GREEN.value)
        screen.blit(new, (self.x, self.y))

        new = pygame.Surface(self.slider_rect.size)
        new.fill(Color.GREEN.value)
        screen.blit(new, self.slider_rect.topleft)

        new = pygame.Surface(self.pointer_rect.size)
        new.fill(Color.GREEN.value)
        screen.blit(new, self.pointer_rect.topleft)


class Label:
    def __init__(self, text, font_size, color, position, visible=True):
        if isinstance(color, Color): color = color.value
        self._text = text
        self._font_size = font_size
        self._color = color
        self._position = position
        self._font = pygame.font.Font(None, self._font_size)
        self.update_surface()
        self._visible = visible

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, str):
            self._text = value
            self.update_surface()
        else:
            raise ValueError("Text must be a string")

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        if isinstance(value, int) and value > 0:
            self._font_size = value
            self._font = pygame.font.Font(None, self._font_size)
            self.update_surface()
        else:
            raise ValueError("Font size must be a positive integer")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, Color): value = value.value #LMAO
        if isinstance(value, tuple) and len(value) == 3:
            self._color = value
            self.update_surface()
        else:
            raise ValueError("Color must be a tuple of three integers")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self._position = value
            self.update_surface()
        else:
            raise ValueError("Position must be a tuple of two integers")

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if isinstance(value, bool):
            if value:
                self._visible = value
        else:
            raise ValueError("Visibility must be a boolean")

    def update_surface(self):
        #updates surface with the correct text and position
        self.surface = self._font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(topleft=self._position)

    def draw(self, screen):
        #draws the label onto the screen
        if self.visible:
            screen.blit(self.surface, self.rect.topleft)

    def rotate(self, angle):
        #rotates the label text by a certain angle
        original_surface = self.surface.copy()
        self.surface = pygame.transform.rotate(original_surface, angle)
        self.rect = self.surface.get_rect(topleft=self._position)

class Chip:
    def __init__(self, position, visible=True):
        self.image_path = "Images/chipBlackWhite_border.png"
        self.original_image = pygame.image.load(self.image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=position)
        self._visible = visible

    @property
    def visible(self):
        return self._visible
    @visible.setter
    def visible(self, value):
        if isinstance(value, bool):
            if value:
                self._visible = value
        else:
            raise ValueError("Visibility must be a boolean")
    def draw(self, screen):
        #draws the chip onto the screen
        if self._visible:
            screen.blit(self.image, self.rect.topleft)

    def change_size(self, scale_factor):
        #changes the size of the chip image
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
    def remove(self, screen):
        new = pygame.Surface(self.rect.size)
        new.fill(Color.GREEN.value)
        screen.blit(new, self.rect.topleft)
