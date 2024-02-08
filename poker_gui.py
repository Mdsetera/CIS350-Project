import pygame
from game_model import *



pygame.init()
window_start_Width = 700
window_start_Height = 700
screen = pygame.display.set_mode((window_start_Width, window_start_Height), pygame.RESIZABLE)
pygame.display.set_caption("Texas Hold'Em!")
clock = pygame.time.Clock()

game = Game()


def change_dimensions(new_Width, new_Height):
    global window_start_Width, window_start_Height

    x_scale = new_Width / window_start_Width
    y_scale = new_Height / window_start_Height

    window_start_Width = new_Width
    window_start_Height = new_Height

    for player in game.seat:
        for card in player.hand:
            card.rect.width = int(card.rect.width * x_scale)
            card.rect.height = int(card.rect.height * y_scale)



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            change_dimensions(event.w, event.h)

    screen.fill((0, 128, 0))

    pygame.display.flip()

    clock.tick(60)

