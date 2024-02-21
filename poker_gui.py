import pygame
from game_model import *



pygame.init()
window_start_Width = 1000
window_start_Height = 750
screen = pygame.display.set_mode((window_start_Width, window_start_Height), pygame.RESIZABLE)
pygame.display.set_caption("Texas Hold'Em!")
clock = pygame.time.Clock()

game = Game()


def initial_deal(game):
    for player in game.active_players:
        while len(player.hand) < 2:
            card = random.choice(game.deck)
            player.hand.append(card)
            game.deck.remove(card)

    for i in range(5):
        card = random.choice(game.deck)
        game.table_cards.append(card)
        game.deck.remove(card)
        i += 1


def show_flop(game):
    if (game.pot != 0) and (game.next_player == game.active_players[0]):
        #once first round of betting is over  (so like preflop)
        flop_1 = game.table_cards[0]
        flip_card1 = pygame.Rect(0, 0, card.width, card.height)
        screen.blit(flop_1.front_image, flip_card1)

        flop_2 = game.table_cards[1]
        flip_card2 = pygame.Rect(0, 0, card.width, card.height)
        screen.blit(flop_2.front_image, flip_card2)

        flop_3 = game.table_cards[2]
        flip_card3 = pygame.Rect(0, 0, card.width, card.height)
        screen.blit(flop_3.front_image, flip_card3)

def show_turn(game):
    if (game.pot != 0) and (game.next_player == game.active_players[0]):
        turn_card = game.table_cards[3]
        flip_turn = pygame.Rect(0, 0, card.width, card.height)
        screen.blit(turn_card.front_image, flip_turn)

def show_river(game):
    if (game.pot != 0) and (game.next_player == game.active_players[0]):
        river_card = game.table_cards[-1]
        flip_river = pygame.Rect(0, 0, card.width, card.height)
        screen.blit(river_card.front_image, flip_river)




#Card Sizes & Position


def create_cards():
    for player in game.active_players:
        #card_spacing = 10

        for j, card in enumerate(player.hand):
            if player == game.active_players[0]:
                if j == 0:
                    player1_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card1.bottomright = (445, 70)
                    screen.blit(card.front_image, player1_card1)
                elif j == 1:
                    player1_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player1_card2.bottomright = (505, 70)
                    screen.blit(card.front_image, player1_card2)
            elif player == game.active_players[1]:
                if j == 0:
                    player2_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card1.bottomright = (0, 380)
                    screen.blit(card.back_image, player2_card1)
                elif j == 1:
                    player2_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player2_card2.bottomright = (0, 320)
                    screen.blit(card.back_image, player2_card2)
            elif player == game.active_players[2]:
                if j == 0:
                    player3_card1 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card1.bottomright = (1000, 430)
                    screen.blit(card.back_image, player3_card1)
                elif j == 1:
                    player3_card2 = pygame.Rect(0, 0, card.width, card.height)
                    player3_card2.bottomright = (1000, 370)
                    screen.blit(card.back_image, player3_card2)



def change_dimensions(new_Width, new_Height):
    global window_start_Width, window_start_Height

    x_scale = new_Width / window_start_Width
    y_scale = new_Height / window_start_Height

    window_start_Width = new_Width
    window_start_Height = new_Height

    for player in game.active_players:
        for card in player.hand:
            card.rect.width = int(card.rect.width * x_scale)
            card.rect.height = int(card.rect.height * y_scale)

            card.front_image = pygame.transform.scale(card.front_image, card.width * x_scale, card.height * y_scale)
            card.back_image = pygame.transform.scale(card.back_image, card.width * x_scale, card.height * y_scale)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            change_dimensions(event.w, event.h)

    screen.fill((0, 128, 0))

    for player in game.active_players:
        for card in player.hand:
            screen.blit(card.front_image, card.rect)

    pygame.display.flip()
    clock.tick(60)

