import os.path

import pygame

window_start_Width = 1000
window_start_Height = 750

buttons = []


##method()
def init_pygame():
    pygame.init()
    global window_start_Width, window_start_Height
    screen = pygame.display.set_mode((window_start_Width, window_start_Height), pygame.RESIZABLE)
    pygame.display.set_caption("Texas Hold'Em!")
    clock = pygame.time.Clock()
    icon_image = pygame.image.load("images\icon.png")
    pygame.display.set_icon(icon_image)

    return screen, clock

# Define a function to create text surface and rect

def show_flop(game, screen):
    #print(game.table_cards)
    #once first round of betting is over  (so like preflop)
    if game.round == 1:
        flop_1 = game.table_cards[0]
        flip_card1 = pygame.Rect(0, 0, flop_1.width, flop_1.height)
        flip_card1.midbottom = (380, 325)
        screen.blit(flop_1.back_image, flip_card1)

        flop_2 = game.table_cards[1]
        flip_card2 = pygame.Rect(0, 0, flop_2.width, flop_2.height)
        flip_card2.midbottom = (440, 325)
        screen.blit(flop_2.back_image, flip_card2)

        flop_3 = game.table_cards[2]
        flip_card3 = pygame.Rect(0, 0, flop_3.width, flop_3.height)
        flip_card3.midbottom = (500, 325)
        screen.blit(flop_3.back_image, flip_card3)
    elif game.round == 2:
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
    screen.fill((0, 128, 0))

    if game.round == 1:
        show_flop(game, screen)
    elif game.round == 2:
        show_turn(game, screen)
    elif game.round == 3:
        show_river(game, screen)

    for player in game.active_players:
        for j, card in enumerate(player.hand):
            if player == game.active_players[0]:
                if j == 0:
                    player1_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card1.topleft = (400, 585)
                    screen.blit(card.front_image, player1_card1)
                elif j == 1:
                    player1_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card2.topleft = (450, 585)
                    screen.blit(card.front_image, player1_card2)
            elif player == game.active_players[1]:
                if j == 0:
                    player2_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card1.topleft = (5, 200)
                    card_rotate1 = pygame.transform.rotate(card.back_image, 90)
                    screen.blit(card_rotate1, player2_card1)
                    #pygame.display.update(player2_card1)
                elif j == 1:
                    player2_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card2.topleft = (5, 250)
                    card_rotate1 = pygame.transform.rotate(card.back_image, 90)
                    screen.blit(card_rotate1, player2_card2)
                    #pygame.display.update(player2_card2)
            elif player == game.active_players[2]:
                if j == 0:
                    player3_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card1.topleft = (840, 200)
                    card_rotate2 = pygame.transform.rotate(card.back_image, 270)
                    screen.blit(card_rotate2, player3_card1)
                elif j == 1:
                    player3_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card2.topleft = (840, 250)
                    card_rotate2 = pygame.transform.rotate(card.back_image, 270)
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
        raise NotImplementedError('need to create way to change button dimensions')
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
    screen.fill((0, 128, 0))
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

class Button():
    def __init__(self, x, y, width, height, text, font_size=20, enabled=True):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.enabled = enabled
        self.font = pygame.font.Font(None, self.font_size)
        buttons.append(self)

    def draw(self, screen):
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
        mouse_pos = pygame.mouse.get_pos()
        x_Overbutton = self.x <= mouse_pos[0] <= self.x + self.width
        y_Overbutton = self.y <= mouse_pos[1] <= self.y + self.height
        return x_Overbutton and y_Overbutton

    def check_click(self, mouse_pos, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_hover(mouse_pos):
                    print(f'clicked \'{self.text}\' button')
                    return True
        return False


class Label:
    def __init__(self, text, font_size, color, position):
        self._text = text
        self._font_size = font_size
        self._color = color
        self._position = position
        self._font = pygame.font.Font(None, self._font_size)
        self.update_surface()

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

    def update_surface(self):
        self.surface = self._font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(topleft=self._position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect.topleft)
