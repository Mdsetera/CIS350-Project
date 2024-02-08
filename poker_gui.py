import pygame
from game_model import *


class GUI:
    pygame.init()
    window_start_Width = 700
    window_start_Height = 700
    screen = pygame.display.set_mode((window_start_Width, window_start_Height))
    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 128, 0))


"""
        # columns = 13
        rows = 4

        for row in range(rows):
            for col in range(columns):
                index = row * columns + col
                if index < len(cards):
                    card = cards[index]
                    card.rect.topleft = (50 + col * (card_width + 10), 150 + row * (card_height + 10))
                    screen.blit(card.front_image, card.rect.topleft)
"""


        pygame.display.flip()
        clock.tick(60)

