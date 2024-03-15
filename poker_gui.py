import os.path

import pygame
from enum import Enum

window_start_Width = 1000
window_start_Height = 750

buttons = []
labels_chip_count = []
labels_player_bet = []
label_pot = []
label_dealer = []
label_current_player_turn = []
label_player_hands = []
class Color(Enum):
    GREEN = (0, 128, 0)
    BLUE = (0,0,255)
    LGREEN = (0, 255, 0)
    RED = (255,0,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
##method()
def init_pygame():
    pygame.init()
    global window_start_Width, window_start_Height
    screen = pygame.display.set_mode((window_start_Width, window_start_Height), pygame.RESIZABLE)
    pygame.display.set_caption("Texas Hold'Em!")
    clock = pygame.time.Clock()
    #icon_image = pygame.image.load("images\icon.png")
    #pygame.display.set_icon(icon_image)

    return screen, clock

# Define a function to create text surface and rect

def show_flop(game, screen):
    #print(game.table_cards)
    #once first round of betting is over  (so like preflop)
    flop_1 = game.table_cards[0]
    flip_card1 = pygame.Rect(0, 0, flop_1.width, flop_1.height)
    flip_card1.midbottom = (380, 325)
    screen.blit(flop_1.front_image, flip_card1)

    flop_2 = game.table_cards[1]
    flip_card2 = pygame.Rect(0, 0, flop_2.width, flop_2.height)
    flip_card2.midbottom = (440, 325)
    screen.blit(flop_2.front_image, flip_card2)

    flop_3 = game.table_cards[2]
    flip_card3 = pygame.Rect(0, 0, flop_3.width, flop_3.height)
    flip_card3.midbottom = (500, 325)
    screen.blit(flop_3.front_image, flip_card3)




def show_turn(game, screen):
    turn_card = game.table_cards[3]
    flip_turn = pygame.Rect(0, 0, turn_card.width, turn_card.height)
    flip_turn.midbottom = (560, 325)
    screen.blit(turn_card.front_image, flip_turn)



def show_river(game, screen):
    river_card = game.table_cards[-1]
    flip_river = pygame.Rect(0, 0, river_card.width, river_card.height)
    flip_river.midbottom = (620, 325)
    screen.blit(river_card.front_image, flip_river)


#Card Sizes & Position
def create_cards(game, screen):

    if game.bet_round >= 2:
        show_flop(game, screen)
    if game.bet_round >= 3:
        show_turn(game, screen)
    if game.bet_round >= 4:
        show_river(game, screen)

#FIXME rerwite to only include active players in release 2
    for player in game.seat:
        for j, card in enumerate(player.hand):
            if player == game.seat[0]:
                if j == 0:
                    player1_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card1.topleft = (5, 200)
                    card_rotate1 = pygame.transform.rotate(card.front_image, 90)
                    screen.blit(card_rotate1, player1_card1)
                elif j == 1:
                    player1_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card2.topleft = (5, 250)
                    card_rotate2 = pygame.transform.rotate(card.front_image, 90)
                    screen.blit(card_rotate2, player1_card2)
            elif player == game.seat[1]:
                if j == 0:
                    player2_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card1.topleft = (400, 585)
                    screen.blit(card.front_image, player2_card1)
                    pygame.display.update(player2_card1)
                elif j == 1:
                    player2_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card2.topleft = (450, 585)
                    screen.blit(card.front_image, player2_card2)
                    pygame.display.update(player2_card2)
            elif player == game.seat[2]:
                if j == 0:
                    player3_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card1.topleft = (840, 200)
                    card_rotate2 = pygame.transform.rotate(card.front_image, 270)
                    screen.blit(card_rotate2, player3_card1)
                elif j == 1:
                    player3_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card2.topleft = (840, 250)
                    card_rotate2 = pygame.transform.rotate(card.front_image, 270)
                    screen.blit(card_rotate2, player3_card2)

    pygame.display.update()


def change_dimensions(game, new_Width, new_Height):
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
    if game.bet_round == 2:
        show_flop(game, screen)
    elif game.bet_round == 3:
        show_turn(game, screen)
    elif game.bet_round == 4:
        show_river(game, screen)

    pygame.display.flip()


def redraw_screen(game, screen, clock):
    screen.fill(Color.GREEN.value)
    update(game, screen, clock)
    pygame.display.flip()


def create_buttons(game):
    fold_button = Button(600, 550, 100, 50, "Fold", 30, False)
    check_button = Button(710, 550, 100, 50, "Check", 30, False)
    call_button = Button(600, 610, 100, 50, "Call", 30, False)
    bet_button = Button(710, 610, 100, 50, "Bet", 30, False)
    fold_button.draw(game.screen)
    check_button.draw(game.screen)
    call_button.draw(game.screen)
    bet_button.draw(game.screen)
    pygame.display.flip()


def enable_buttons(game, player):
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
    import hand_rank_tests as rank
    global labels_chip_count,labels_player_bet, label_pot, label_dealer, label_current_player_turn
    labels_chip_count = []
    labels_player_bet = []
    label_pot = []
    label_dealer = []
    label_current_player_turn = []

    l_dealer = Label(f"Dealer: Player {game.dealer_seat}", 40, (0, 0, 0), (5, 5))
    l_dealer.draw(game.screen)
    label_dealer.append(l_dealer)

    label0_text = f'Player 0 Balance: {int(game.seat[0].chips)}'
    label0_bet_text = f'Player 0 Bet: {int(game.seat[0].bet)}'
    label0_hand_text = game.seat[0].get_hand_rank_str()
    #Player 0 labels
    player0_balance = Label(label0_text, 25, Color.LGREEN, (45, 370))
    player0_bet = Label(label0_bet_text, 25, Color.LGREEN, (10, 370))
    player0_hand = Label(label0_hand_text, 25, Color.LGREEN, (80, 370))
    label_player_hands.append(player0_hand)
    labels_chip_count.append(player0_balance)
    labels_player_bet.append(player0_bet)

    label1_text = f'Player 1 Balance: {int(game.seat[1].chips)}'
    label1_bet_text = f'Player 1 Bet: {int(game.seat[1].bet)}'
    label1_hand_text = game.seat[1].get_hand_rank_str()
    #Player 1 labels
    player1_balance = Label(label1_text, 40, Color.LGREEN, (565, 670))
    player1_bet = Label(label1_bet_text, 40, Color.LGREEN, (565, 710))
    player1_hand = Label(label1_hand_text, 40, Color.LGREEN, (420, 550))
    label_player_hands.append(player1_hand)
    labels_chip_count.append(player1_balance)
    labels_player_bet.append(player1_bet)

    label2_text = f'Player 2 Balance: {int(game.seat[2].chips)}'
    label2_bet_text = f'Player 2 Bet: {int(game.seat[2].bet)}'
    label2_hand_text = game.seat[2].get_hand_rank_str()
    #Player 2 labels

    player2_balance = Label(label2_text, 25, Color.LGREEN, (930, 410))
    player2_bet = Label(label2_bet_text, 25, Color.LGREEN, (965, 480))
    player2_hand = Label(label2_hand_text, 25, Color.LGREEN, (895, 480))
    label_player_hands.append(player2_hand)
    labels_chip_count.append(player2_balance)
    labels_player_bet.append(player2_bet)

    player0_balance.rotate(270)
    player0_bet.rotate(270)
    player0_hand.rotate(270)
    player2_balance.rotate(90)
    player2_bet.rotate(90)
    player2_hand.rotate(90)

    player0_balance.draw(game.screen)
    player0_bet.draw(game.screen)
    player0_hand.draw(game.screen)
    player1_balance.draw(game.screen)
    player1_bet.draw(game.screen)
    player1_hand.draw(game.screen)
    player2_balance.draw(game.screen)
    player2_bet.draw(game.screen)
    player2_hand.draw(game.screen)

    chip1_player0 = Chip((38, 560))
    chip2_player0 = Chip((5, 530))
    chip1_player0.change_size(.5)
    chip2_player0.change_size(.5)

    chip1_player1 = Chip((880, 660))
    chip2_player1 = Chip((800, 700))
    chip1_player1.change_size(.6)
    chip2_player1.change_size(.6)

    chip1_player2 = Chip((920, 370))
    chip2_player2 = Chip((955, 415))
    chip1_player2.change_size(.5)
    chip2_player2.change_size(.5)

    chip1_player0.draw(game.screen)
    chip2_player0.draw(game.screen)
    chip1_player1.draw(game.screen)
    chip2_player1.draw(game.screen)
    chip1_player2.draw(game.screen)
    chip2_player2.draw(game.screen)

    #pot label
    label_pot.append(Label(f"Pot: 0", 40, Color.RED, (430, 370)))
    total_pot = 0
    for pot in game.pot:
        total_pot += pot
    label_pot[0].text = f'Pot: {total_pot}'
    #label_pot[0].visible = total_pot > 0 #toggle visibility
    label_pot[0].draw(game.screen)

    label_current_player_turn.append(Label(f'{game.current_player}\'s turn', 40, Color.BLACK, (5, 40)))
    label_current_player_turn[0].draw(game.screen)

    #fold lables
    label_fold = []
    #print("Players in seats ->", game.seat)
    #print(f"[{game.seat[0].fold},{game.seat[1].fold},{game.seat[2].fold}]")
    label_fold.append(Label('FOLD', 60, Color.BLACK, (5+10,200+30), visible = game.seat[0].fold))
    label_fold[0].rotate(20)

    label_fold[0].draw(game.screen)

    label_fold.append(Label('FOLD', 60, Color.BLACK, (405+10,585+30), visible = game.seat[1].fold))
    label_fold[1].rotate(20)
    label_fold[1].draw(game.screen)

    label_fold.append(Label('FOLD', 60, Color.BLACK, (840+10,200+30), visible = game.seat[2].fold))
    label_fold[2].rotate(20)
    label_fold[2].draw(game.screen)

    #print(f'{label_fold[0].visible},{label_fold[1].visible},{label_fold[2].visible}')
    #all in lables
    label_player_all_in = []
    label_player_all_in.append(Label('ALL IN', 60, Color.BLACK, (5+10,200+30), visible = game.seat[0].all_in))
    label_player_all_in[0].rotate(20)
    label_player_all_in[0].draw(game.screen)

    label_player_all_in.append(Label('ALL IN', 60, Color.BLACK, (405+10,585+30), visible = game.seat[1].all_in))
    label_player_all_in[1].rotate(20)
    label_player_all_in[1].draw(game.screen)

    label_player_all_in.append(Label('ALL IN', 60, Color.BLACK, (840+10,200+30), visible = game.seat[2].all_in))
    label_player_all_in[2].rotate(20)
    label_player_all_in[2].draw(game.screen)




    pygame.display.flip()


def update_labels(game):
    #reset all labels used in the game
    #erase label text by redrawing
    for label in labels_chip_count + labels_player_bet + label_pot + label_dealer + label_current_player_turn + label_player_hands:
        new = pygame.Surface(label.rect.size)
        new.fill(Color.GREEN.value)
        game.screen.blit(new, label.rect.topleft)
    #set labels to new text
    create_labels(game)


    pygame.display.flip()

def print_winner(screen, winner):
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
        #mouse_pos = pygame.mouse.get_pos()
        x_Overbutton = self.x <= mouse_pos[0] <= self.x + self.width
        y_Overbutton = self.y <= mouse_pos[1] <= self.y + self.height
        #print(f'Hover check for button\'{self.text}\': {x_Overbutton and y_Overbutton}')
        return x_Overbutton and y_Overbutton

    def check_click(self, mouse_pos, events):
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
        #draw slider bar
        pygame.draw.rect(screen, (200, 200, 200), self.slider_rect)
        #draw slider pointer
        pygame.draw.rect(screen, (0, 0, 0), self.pointer_rect)

        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y + self.height + 5, self.width, 15))
        #draw value
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.value), True, (0, 0, 0))

        screen.blit(text, (self.x + self.width // 2, self.y + self.height + 5))

    def handle_click(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.pointer_rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True

    def handle_drag(self, mouse_pos):
        if self.dragging:
            mouse_x, mouse_y = mouse_pos

            pointer_x = max(self.x, min(mouse_x - self.pointer_rect.width // 2, self.x + self.width))
            self.pointer_rect.x = pointer_x

            # Calculate the position of the pointer relative to the slider's width
            relative_pos = 1 - ((pointer_x - self.x) / self.width)
            # Update the value accordingly
            self.value = int(relative_pos * (self.maximum - self.minimum) / self.step) * self.step + self.minimum

    def handle_release(self):
        self.dragging = False

    def move_slider(self, mouse_pos):
        self.pointer_rect.centerx = mouse_pos[0]


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
        self.surface = self._font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(topleft=self._position)

    def draw(self, screen):
        if self.visible:
            screen.blit(self.surface, self.rect.topleft)

    def rotate(self, angle):
        original_surface = self.surface.copy()
        self.surface = pygame.transform.rotate(original_surface, angle)
        self.rect = self.surface.get_rect(topleft=self._position)

class Chip:
    def __init__(self, position):
        self.image_path = "Images/chipBlackWhite_border.png"
        self.original_image = pygame.image.load(self.image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def change_size(self, scale_factor):
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
