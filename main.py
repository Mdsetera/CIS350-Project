import random
import pygame
from game_model import Game
import poker_gui as gui


def main():
    #Initialize game instance
    game = Game(num_User_players=3, num_AI_players=0)
    print('shitter')
    screen, clock = gui.init_pygame()
    fold_button = gui.Button(600, 550, 100, 50, "Fold", 30, True)
    fold_button.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                gui.change_dimensions(game, event.w, event.h)
                gui.update(game, screen, clock)
                pygame.display.flip()
                gui.redraw_screen(game, screen, clock)
                gui.create_cards(game, screen)

        while not game.check_end_game():
            game.round += 1
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_first_round_bets()


        fold_button.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
