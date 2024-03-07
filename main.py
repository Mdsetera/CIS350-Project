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
            elif event.type -- pygame.FULLSCREEN:
                print('fullscreened')


        while not game.check_end_game():
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_blinds()
            take_bets(game)
            game.update_pot()
            gui.show_flop(game, game.screen)
            game.add_flop_cards()
            #second round of bets
            print('second round of bets')
            take_bets(game)



        pygame.display.flip()

    pygame.quit()
def take_bets(game:Game):
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

    #fold button
    fold_button = gui.Button(600, 550, 100, 50, "Fold", 30, True)
    if moves['fold'] == False: fold_button.enabled = False
    fold_button.draw(game.screen)
    #check button
    check_button = gui.Button(710, 550, 100, 50, "Check", 30, True)
    if moves['check'] == False: check_button.enabled = False
    check_button.draw(game.screen)
    #call button
    call_button = gui.Button(600, 610, 100, 50, "Call", 30, True)
    if moves['call'] == False: call_button.enabled = False
    call_button.draw(game.screen)
    #bet button
    bet_button = gui.Button(710, 610, 100, 50, "Bet", 30, True)
    if moves['bet'] == False: bet_button.enabled = False
    bet_button.draw(game.screen)
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
        if (fold_button.check_click(mouse_pos, events)):
            print('clicked fold button')
            return ('fold', 0)
        # elif (game.check_button.check_click(mouse_pos, events)) and moves['check'] is True:
        #     return ('check', player.bet)
        # elif (game.call_button.check_click(mouse_pos, events)) and moves['call'] is True:
        #     return ('call', player.bet)
        # elif (game.bet_button.check_click(mouse_pos, events)) and moves['bet'] is True:
        #     return ('bet', player.bet)
    return ('no input received', 0)
def resize_video(game:Game, screen, clock):
    pass

if __name__ == '__main__':
    main()
