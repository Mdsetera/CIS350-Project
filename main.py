import copy
import random
import pygame
import poker_gui as gui
from start_screen import start_screen
from game_model import Game, Player, UserPlayer


screen, clock = gui.init_pygame()


def main():
    """
    Main will create and run the game and gui
    :return:
    """
    #Initialize game instance
    game = Game(num_User_players=1)
    screen, clock = gui.init_pygame()
    screen.fill((0, 128, 0))
    gui.create_buttons(game)
    gui.create_labels(game)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
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
#vvvvvvvvvvvvvvvvv The GAME LOOP vvvvvvvvvvvvvvvvv#
        while not game.check_end_game():
            game.screen.fill(gui.Color.GREEN.value)
            game.start_round(game.screen)
            game.deal_initial_cards()
            game.take_blinds()
            print('first round of bets')
            pygame.display.flip()
            take_bets(game)
            game.update_pot()
            gui.update_labels(game)
            if game.check_end_round():
                gui.update_labels(game)
                winner = game.active_players[0]
                game.end_round([winner])
                continue
            print('heres the flop')
            gui.show_flop(game, game.screen)
            game.add_flop_cards()
            gui.update_labels(game)
            #second round of bets
            print('second round of bets')
            take_bets(game)
            game.update_pot()
            gui.update_labels(game)
            if game.check_end_round():
                winner = game.active_players[0]
                game.end_round([winner])
                continue
            print('heres the turn')
            gui.show_turn(game, game.screen)
            game.add_turn_cards()
            gui.update_labels(game)
            print('third round of bets')
            take_bets(game)
            game.update_pot()
            gui.update_labels(game)
            if game.check_end_round():
                winner = game.active_players[0]
                game.end_round([winner])
                continue
            print('heres the river')
            gui.show_river(game, game.screen)
            game.add_river_cards()
            gui.update_labels(game)
            print('last round of bets')
            take_bets(game)
            game.update_pot()
            gui.update_labels(game)
            if game.check_end_round():
                winner = game.active_players[0]
                game.end_round([winner])
                continue
            print('comparing hands and selecting winner')
            winners = game.compare_hands(game.active_players)
            game.end_round(winners)
            game.update_pot()
            gui.update_labels(game)

        print('game loop has ended')
#^^^^^^^^^^^^^^^ The GAME LOOP ^^^^^^^^^^^^^^^#
        pygame.display.flip()
        winner = None
        for player in game.seat:
            if player.chips > 0:
                if winner != None: raise ValueError('cannot have two winners')
                winner = player
                print('winner is', player.__str__())
                gui.print_winner(game.screen, player)
                break
        pygame.time.delay(5000)
        running = False
        pygame.quit()
        exit()
def take_bets(game:Game):
    """
    this method takes the current active players
    and performs a round of bets
    the round ends when everyone has played
    and all the bets are equal
    or if everyone folds but one player

    :param game:
    :return:
    """
    game.bet_round+=1
    gui.update_labels(game)
    game.update_highest_bet()
    turn_not_taken = []
    everyone_took_turn = False
    game.active_players = [player for player in game.seat if (player.chips > 0 and not player.fold)]
    print(f'Round {game.round} active players -> {game.active_players}')
    for player in game.active_players: turn_not_taken.append(player)
    while not (game.equal_bets() and not turn_not_taken) and len(game.active_players) > 1:
        player = game.current_player
        if isinstance(player, UserPlayer):
            game.current_player = game.next_player(player) # switches player before they make a move
            print(f'{player}\'s turn')                                                            # because fold removes them from active players
            player._play(game, get_player_input(game, player)) #Userplayer
        else:
            #FIXME implement a small timer for the computer turns
            print(f'{player}\'s turn')
            delay(2) #in seconds
            game.current_player = game.next_player(player)
            player._play(game) #AI player
        if player in turn_not_taken: turn_not_taken.remove(player)
        print(f'turn not taken -> {turn_not_taken}')
        gui.update_labels(game)
        print("active players after turn",  game.active_players)

def get_player_input(game: Game, player: Player) -> (str,int):
    """
    this function will utilize the gui buttons to determine
    what move the player will make
    it will then return what move the player made,
    and the amount of chips associated with that move
    :param game:
    :param player: current players turn, input received will affect this player
    :return: (move, amount)
    """
    #gets current player
    print('getting input from player', player)
    gui.enable_buttons(game, player)
    input_received = False
    betslider = None
    submit_button = gui.Button(630, 590, 80, 30, "Submit Bet", 20, True, visible=False)
    cancel_button = gui.Button(720, 590, 80, 30, "Cancel", 20, True, visible=False)
    #creating event to track timer
    TIMEREVENT = pygame.USEREVENT + 1
    #create_timer
    pygame.time.set_timer(TIMEREVENT, 1000)
    countdown_time = 99 #length of the timer in seconds DONT GO OVER 99 causes render issues
    num_time_passed = 0
    font = pygame.font.Font(None, 55)

    while(input_received == False):
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
                gui.update_labels(game)
            elif event.type == TIMEREVENT:
                countdown_time -= 1
                num_time_passed += 1
                #print(num_time_passed)
                if countdown_time <= 0:
                    input_received = True
                    return ('fold', 0)
                elif num_time_passed >= 3 and player.all_in:
                    return ('check', 0)

        timer_positions = [(250,465),(140,255),(470,50),(625,255)]
        pos = timer_positions[game.seat.index(player)]
        #create rect to clear the timer space before incrementing countdown to prevent overlapping
        timer_rect = pygame.Rect(pos[0], pos[1],50, 50)
        game.screen.fill((0, 128, 0), timer_rect)

        #update timer while no input recieved
        timer_text = font.render(str(countdown_time), True, (255, 255, 255))
        game.screen.blit(timer_text, pos)
        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        #events = pygame.event.get()
        for button in gui.buttons:
            if button.check_click(mouse_pos, events):
                if button.text == "Fold" and button.enabled:
                    game.screen.fill((0, 128, 0), timer_rect)
                    if betslider:betslider.remove(game.screen)
                    return ('fold', 0)
                elif button.text == "Check" and button.enabled:
                    game.screen.fill((0, 128, 0), timer_rect)
                    if betslider:betslider.remove(game.screen)
                    return ('check', 0)
                elif button.text == 'Call' and button.enabled:
                    game.screen.fill((0, 128, 0), timer_rect)
                    if betslider:betslider.remove(game.screen)
                    return ('call', 0)
                elif button.text == 'Bet' and button.enabled:
                    range = player.get_bet_range(game)
                    betslider = gui.Slider(600, 580, 200, 20, range[0], range[1], 10, visible=True)

        if betslider:
            betslider.draw(game.screen)
            submit_button.visible = True
            cancel_button.visible = True
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
                        submit_button.visible = False
                        cancel_button.visible = False
                        submit_button.remove(game.screen)
                        cancel_button.remove(game.screen)
                        gui.redraw_screen(game, game.screen, clock)
                        gui.create_cards(game, game.screen)
                        gui.create_buttons(game)
                        gui.update_labels(game)
                        pygame.display.flip()
                        input_received = True
                        game.screen.fill((0, 128, 0), timer_rect)
                        return ('bet', playerbet)
                    if cancel_button.check_click(mouse_pos, events):
                        betslider = None
                        submit_button.visible = False
                        cancel_button.visible = False
                        gui.redraw_screen(game, game.screen, clock)
                        gui.create_cards(game, game.screen)
                        submit_button.remove(game.screen)
                        cancel_button.remove(game.screen)
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
        else:
            submit_button.remove(game.screen)
            cancel_button.remove(game.screen)


    pygame.time.set_timer(TIMEREVENT, 0)
    raise ValueError('no input received')
    return ('fold', 0)

def delay(seconds:int):
    # creating event to track timer
    TIMEREVENT = pygame.USEREVENT + 2
    # create_timer
    pygame.time.set_timer(TIMEREVENT, 1000)
    while seconds > 0:
        events = pygame.event.get()
        for event in events:
            if event.type == TIMEREVENT:
                seconds -= 1
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
    pass
def print_winners(winners):
    for p in winners:
        print(p, 'takes the hand')
    #winner_label = Label()

if __name__ == '__main__':
    if start_screen() == 0:
        main()
    else:
        main()#FIXME delete when blackjack mode is complete
        #blackjack()

