import random
import pygame
from game_model import Game, Player, UserPlayer
import poker_gui as gui


def main():
    #Initialize game instance
    game = Game(num_User_players=3, num_AI_players=0)
    print('shitter')
    screen, clock = gui.init_pygame()
    #fold_button = gui.Button(600, 550, 100, 50, "Fold", 30, True)
    #fold_button.draw(screen)
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
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_blinds()
            take_first_round_bets(game)
            game.update_pot()
            gui.show_flop(game, game.screen)
            game.add_flop_cards()

        pygame.display.flip()

    pygame.quit()
def take_first_round_bets(game:Game):
    while not game.equal_bets():
        for player in game.active_players:
            if type(player) is type(UserPlayer):
                player._play(game, get_player_input(game, player))
            else:
                player._play(game)


def get_player_input(game: Game, player: Player) -> (int,int):
    #gets current player
    #return (move, bet_amount) ex. ('bet', 50)
    #moves = {"fold": True, "check": False, "call": False, "bet": False}
    fold_button = gui.Button(600, 550, 100, 50, "Fold", 30, True)
    fold_button.draw(game.screen)
    moves = player.get_moves(game)
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    if (fold_button.check_click(mouse_pos, events)) and moves['fold'] is True:
        return ('fold', 0)
    elif (game.check_button.check_click(mouse_pos, events)) and moves['check'] is True:
        return ('check', player.bet)
    elif (game.call_button.check_click(mouse_pos, events)) and moves['call'] is True:
        return ('call', player.bet)
    elif (game.bet_button.check_click(mouse_pos, events)) and moves['bet'] is True:
        return ('bet', player.bet)


if __name__ == '__main__':
    main()
