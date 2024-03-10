import random
import pygame
from game_model import Game, Player, UserPlayer
import poker_gui as gui

screen, clock = gui.init_pygame()
def main():
    #Initialize game instance
    game = Game(num_User_players=3, num_AI_players=0)
    screen, clock = gui.init_pygame()
    screen.fill((0, 128, 0))
    gui.create_buttons(game)
    gui.create_labels(game)
    label_dealer = gui.Label(f"Dealer: Player {game.dealer_seat}", 20, gui.Color.BLUE.value, (5, 120))
    label_dealer.draw(game.screen)

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
                gui.create_buttons(game)
                gui.create_labels(game)
            elif event.type == pygame.FULLSCREEN:
                print('fullscreened')


        while not game.check_end_game():
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_blinds()
            print('first round of bets')
            pygame.display.flip()
            take_bets(game)
            game.update_pot()
            if game.check_end_round():

                winner = game.active_players[0]
                game.end_round([winner])
                pass
            print('heres the flop')
            gui.show_flop(game, game.screen)
            game.add_flop_cards()
            #second round of bets
            print('second round of bets')
            take_bets(game)
            game.update_pot()
            if game.check_end_round():
                winner = game.active_players[0]
                game.end_round([winner])
                pass


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
            gui.update_labels(game)
            if game.equal_bets():
                break


def get_player_input(game: Game, player: Player) -> (int,int):
    #gets current player
    #return (move, bet_amount) ex. ('bet', 50)
    print('getting input from player', game.seat.index(player)+1)
    gui.enable_buttons(game, player)
    input_received = False
    betslider = None
    submit_button = None
    cancel_button = None
    #creating event to track timer
    TIMEREVENT = pygame.USEREVENT + 1
    #create timer
    pygame.time.set_timer(TIMEREVENT, 1000)
    countdown_time = 25
    font = pygame.font.Font(None, 55)

    while(input_received == False):#FIXME turn this while loop into a timer, when timer ends return ('fold', 0)
        events = pygame.event.get()
        for event in events:
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
            elif event.type == TIMEREVENT:
                countdown_time -= 1
                if countdown_time <= 0:
                    input_received = True
                    return ('fold', 0)

        #create rect to clear the timer space before incrementing countdown to prevent overlapping
        timer_rect = pygame.Rect(460, 25, 100, 55)
        game.screen.fill((0, 128, 0), timer_rect)

        #update timer while no input recieved
        timer_text = font.render(str(countdown_time), True, (255, 255, 255))
        game.screen.blit(timer_text, (460, 25))
        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        #events = pygame.event.get()
        for button in gui.buttons:
            if button.check_click(mouse_pos, events):
                if button.text == "Fold":
                    return ('fold', 0)
                elif button.text == "Check":
                    return ('check', 0)
                elif button.text == 'Call':
                    return ('call', 0)
                elif button.text == 'Bet':
                    betslider = gui.Slider(700, 500, 200, 20, 0, 1100, 10)
                    submit_button = gui.Button(700, 460, 80, 30, "Submit Bet", 20, True)
                    cancel_button = gui.Button(800, 460, 80, 30, "Cancel", 20, True)

        if betslider:
            betslider.draw(game.screen)
            submit_button.draw(game.screen)
            cancel_button.draw(game.screen)
            pygame.display.flip()

            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if betslider.handle_click(mouse_pos):
                        betslider.dragging = True
                    if submit_button.check_click(mouse_pos, events):
                        playerbet = betslider.value
                        betslider = None
                        submit_button = None
                        cancel_button = None
                        gui.redraw_screen(game, game.screen, clock)
                        gui.create_cards(game, game.screen)
                        gui.create_buttons(game)
                        gui.update_labels(game)
                        pygame.display.flip()
                        input_received = True
                        return ('bet', playerbet)
                    if cancel_button.check_click(mouse_pos, events):
                        betslider = None
                        submit_button = None
                        cancel_button = None
                        gui.redraw_screen(game, game.screen, clock)
                        gui.create_cards(game, game.screen)
                        gui.create_buttons(game)
                        gui.update_labels(game)
                        pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if betslider.dragging:
                        betslider.dragging = False
                if betslider and betslider.dragging:
                    betslider.handle_drag(mouse_pos)
                    pygame.display.flip()
                    betslider.draw(game.screen)
                    pygame.display.flip()

            pygame.time.Clock().tick(60)

    pygame.time.set_timer(TIMEREVENT, 0)
    raise ValueError('no input received')
    return ('fold', 0)
def resize_video(game:Game, screen, clock):
    pass

if __name__ == '__main__':
    main()
