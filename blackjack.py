import pygame
import game_model
from game_model import Deck, Card, Suit

window_start_width = 805
window_start_height = 685
stage_bet = "bet"
stage_play = "play"
current_stage = stage_bet

def init_pygame():
    """
    Initializes the game window and returns the screen and clock objects.
    """
    pygame.init()
    screen = pygame.display.set_mode((window_start_width, window_start_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Blackjack!")
    clock = pygame.time.Clock()
    return screen, clock


def show_cards(screen, deck):
    for card in deck.stack:
        screen.blit(card.back_image, (100, 220))


def deal_cards(screen, card, target_position, speed=10):
    # Initialize the clock for controlling frame rate
    clock = pygame.time.Clock()

    # Calculate initial x and y differences
    x_difference = target_position[0] - card.rect.x
    y_difference = target_position[1] - card.rect.y


    # Handle horizontal movement first
    while abs(x_difference) > speed:
        # Clear the card's current position area using the background color
        pygame.draw.rect(screen, (139, 0, 0), card.rect)

        # Update the card's x position incrementally
        if x_difference > 0:
            card.rect.x += speed
        else:
            card.rect.x -= speed
        screen.blit(card.back_image, (100, 220))
        # Update the x difference
        x_difference = target_position[0] - card.rect.x

        # Draw the card at its new x position
        screen.blit(card.front_image, card.rect)

        # Control the frame rate for smooth animation
        clock.tick(60)

        pygame.display.update()

    # Now handle vertical movement
    while abs(y_difference) > speed:
        screen.blit(card.back_image, (100, 220))
        # Clear the card's current position area using the background color
        pygame.draw.rect(screen, (139, 0, 0), card.rect)

        # Update the card's y position incrementally
        if y_difference > 0:
            card.rect.y += speed
        else:
            card.rect.y -= speed

        # Update the y difference
        y_difference = target_position[1] - card.rect.y

        # Draw the card at its new y position
        screen.blit(card.front_image, card.rect)

        # Control the frame rate for smooth animation
        clock.tick(60)

        pygame.display.update()

    # Once the card reaches the target position, set the final position
    card.rect.topleft = target_position

    # Clear the card's final position area using the background color
    pygame.draw.rect(screen, (139, 0, 0), card.rect)

    # Draw the card in its final position on the screen
    screen.blit(card.front_image, card.rect)

    # Update the display to reflect the final state
    pygame.display.flip()


def create_bet_buttons(screen):
    font = pygame.font.Font(None, 36)

    fivehundred_button = pygame.Rect(60, 630, 80, 50)
    twentyfive_button = pygame.Rect(500, 630, 80, 50)
    fifty_button = pygame.Rect(350, 630, 80, 50)
    onehundred_button = pygame.Rect(200, 630, 80, 50)
    five_button = pygame.Rect(650, 630, 80, 50)

    global bet_button_list
    bet_button_list = []
    pygame.draw.rect(screen, (0, 0, 0), fivehundred_button)
    pygame.draw.rect(screen, (0, 0, 0), onehundred_button)
    pygame.draw.rect(screen, (0, 0, 0), fifty_button)
    pygame.draw.rect(screen, (0, 0, 0), twentyfive_button)
    pygame.draw.rect(screen, (0, 0, 0), five_button)

    five_text = font.render("5", True, (255, 255, 255))
    twentyfive_text = font.render("25", True, (255, 255, 255))
    fifty_text = font.render("50", True, (255, 255, 255))
    onehundred_text = font.render("100", True, (255, 255, 255))
    fivehundred_text = font.render("500", True, (255, 255, 255))

    screen.blit(onehundred_text, (525, 645))
    screen.blit(twentyfive_text, (210, 645))
    screen.blit(fifty_text, (355, 645))
    screen.blit(fivehundred_text, (673, 645))
    screen.blit(five_text, (75, 645))
    pygame.display.flip()

    return fivehundred_button, onehundred_button, fifty_button, twentyfive_button, five_button


def create_buttons(screen):
    font = pygame.font.Font(None, 36)

    hit_button = pygame.Rect(500, 630, 80, 50)
    stand_button = pygame.Rect(350, 630, 80, 50)
    split_button = pygame.Rect(200, 630, 80, 50)

    global button_list
    button_list = [hit_button, stand_button, split_button]
    pygame.draw.rect(screen, (0, 0, 0), hit_button)
    pygame.draw.rect(screen, (0, 0, 0), stand_button)
    pygame.draw.rect(screen, (0, 0, 0), split_button)

    hit_text = font.render("Hit", True, (255, 255, 255))
    stand_text = font.render("Stand", True, (255, 255, 255))
    split_text = font.render("Split", True, (255, 255, 255))

    screen.blit(hit_text, (525, 645))
    screen.blit(stand_text, (355, 645))
    screen.blit(split_text, (210, 645))
    pygame.display.flip()

    return hit_button, stand_button, split_button


def handle_hit(player, deck, screen):
    hitcount = 0
    if len(deck.stack) > 0:
        # Take the top card from the deck
        new_card = deck.stack.pop(0)
        # Add the new card to the player's hand
        player.append(new_card)
        print('HIT! New card dealt to player.')
        print(player)
        hitcount += 1
    else:
        print('No more cards left in the deck.')
    playerscore = calculate_scores(player)
    if playerscore > 21:
        print("You busted! You Lose!")




def handle_stand(dealer, player, deck):
    dealer_score = calculate_scores(dealer)
    player_score = calculate_scores(player)
    while dealer_score < 17:
        if len(deck.stack) > 0:
            new_card = deck.stack.pop(0)
            dealer.append(new_card)
            dealer_score = calculate_scores(dealer)

    if (dealer_score > 21) and (player_score <= 21):
        print("Dealer busts! You Win!")
    elif (dealer_score == 21) and (player_score < 21):
        print("Dealer has Blackjack! You lose!")
    elif (dealer_score > player_score) and (dealer_score <= 21):
        print("You Lose!")
    elif (player_score > dealer_score) and (player_score <= 21):
        print("You Win!")
    elif player_score == dealer_score:
        print("Push!")

    return dealer_score






def calculate_scores(player):
    playerscore = 0
    count_aces = 0
    for card in player:
        if card.value == 11:
            playerscore += 10
        elif card.value == 12:
            playerscore += 10
        elif card.value == 13:
            playerscore += 10
        elif card.value == 14:
            playerscore += 11
            count_aces += 1
        else:
            playerscore += card.value

    while playerscore > 21 and count_aces > 0:
        playerscore -= 10
        count_aces -= 1

    return playerscore




#def get_player_bet():



def game():
    global current_stage
    global playerchips
    global playerbet
    global player
    global dealer
    playerchips = 1000
    playerbet = 0
    player = []
    dealer = []
    screen, clock = init_pygame()
    running = True
    deck = Deck()
    deck.shuffle()

    # Initialize the positions of the cards
    for card in deck.stack:
        card.rect.topleft = (100, 280)

    # Deal initial cards to player and dealer
    player.append(deck.stack.pop(0))
    dealer.append(deck.stack.pop(0))
    player.append(deck.stack.pop(0))
    dealer.append(deck.stack.pop(0))
    print(player, dealer)
    # Create buttons
    five_button, twentyfive_button, fifty_button, onehundred_button, fivehundred_button = create_bet_buttons(screen)
    hit_button, stand_button, split_button = create_buttons(screen)

    # Game loop
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle bet phase
                if current_stage == stage_bet:
                    # Handle bet button clicks
                    if five_button.collidepoint(event.pos):
                        playerbet = 5
                        playerchips -= 5
                    elif twentyfive_button.collidepoint(event.pos):
                        playerbet = 25
                        playerchips -= 25
                    elif fifty_button.collidepoint(event.pos):
                        playerbet = 50
                        playerchips -= 50
                    elif onehundred_button.collidepoint(event.pos):
                        playerbet = 100
                        playerchips -= 100
                    elif fivehundred_button.collidepoint(event.pos):
                        playerbet = 500
                        playerchips -= 500

                    # Transition to the play phase
                    current_stage = stage_play

                # Handle play phase
                elif current_stage == stage_play:
                    if hit_button.collidepoint(event.pos):
                        handle_hit(player, deck, screen)
                    elif stand_button.collidepoint(event.pos):
                        handle_stand(dealer, player, deck)


        # Clear the screen
        screen.fill((139, 0, 0))
        show_cards(screen, deck)
        # Redraw game elements based on the current stage
        if current_stage == stage_bet:
            # Create and display bet buttons
            create_bet_buttons(screen)
        elif current_stage == stage_play:
            # Create and display hit, stand, and split buttons
            create_buttons(screen)
            calculate_scores(player)
            calculate_scores(dealer)
        # Redraw the cards on the table for both player and dealer
        for i, card in enumerate(player):
            deal_cards(screen, card, (145 + 100 * i, 455), speed=10)
        for i, card in enumerate(dealer):
            deal_cards(screen, card, (145 + 100 * i, 15), speed=10)



        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Clean up and exit
    pygame.quit()
# Run the main function to start the game loop
if __name__ == '__main__':
    game()

