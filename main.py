import random
import pygame
from game_model import Game, Player, UserPlayer
import poker_gui as gui

screen, clock = gui.init_pygame()
def main():
    #Initialize game instance
    game = Game(num_User_players=3, num_AI_players=0)
    print('shitter')
    screen, clock = gui.init_pygame()
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
            elif event.type == pygame.FULLSCREEN:
                print('fullscreened')


        while not game.check_end_game():
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_blinds()
            print('first round of bets')
            take_bets(game)
            game.update_pot()
            print('heres the flop')
            gui.show_flop(game, game.screen)
            game.add_flop_cards()
            #second round of bets
            print('second round of bets')
            take_bets(game)



        pygame.display.flip()

    pygame.quit()
def take_bets(game:Game):
    game.bet_round+=1
    while not game.equal_bets():
        for player in game.active_players:
            if type(player) is type(UserPlayer()):
                player._play(game, get_player_input(game, player))
            else:
                player._play(game)
            if game.equal_bets():
                break


def get_player_input(game: Game, player: Player) -> (int,int):
    #gets current player
    #return (move, bet_amount) ex. ('bet', 50)
    #moves = {"fold": True, "check": False, "call": False, "bet": False}
    print('getting input from player', game.seat.index(player)+1)
    moves = player.get_moves(game)

    pygame.display.flip()
    input_received = False
    while(input_received == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                gui.change_dimensions(game, event.w, event.h)
                gui.update(game, screen, clock)
                pygame.display.flip()
                gui.redraw_screen(game, screen, clock)
                gui.create_cards(game, screen)

        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for button in gui.buttons:
            if (button.check_click(mouse_pos, events)):
                if button.text == "Fold":
                    return ('fold', 0)
                elif button.text == "Check":
                    return ('check', 0)
                elif button.text == 'Call':
                    return ('call', 0)
                elif button.text == 'Bet':
                    bet_amount = 20 #FIXME get bet amount from slider
                    return ('bet', bet_amount)

    return ('no input received', 0)
def resize_video(game:Game, screen, clock):
    pass

if __name__ == '__main__':
    main()
