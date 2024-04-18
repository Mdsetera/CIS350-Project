import pygame
import game_model
from game_model import Deck, Card, Suit

window_start_width = 805
window_start_height = 685
stage_bet = "bet"
stage_play = "play"
current_stage = stage_bet
dealers_card_face_down = True


def init_pygame():
    """
    Initializes the game window and returns the screen and clock objects.
    """
    pygame.init()
    screen = pygame.display.set_mode((window_start_width, window_start_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Blackjack!")
    clock = pygame.time.Clock()
    return screen, clock

def player_blackjack(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("You have 21! You win!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (180, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()


def dealer_blackjack(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("Dealer has blackjack! You lose!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (180, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()


def player_busted_message(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("You busted! You lose!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (180, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()


def dealer_busted_message(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("Dealer busted! You win!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (180, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()

def player_loses(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("You Lose!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (300, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()


def player_wins(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("You Win!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (300, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()


def push_message(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 58)

    player_bjmessage = font.render("Push! Try Again!", True, (255, 255, 255))
    screen.blit(player_bjmessage, (150, 300))
    pygame.display.update()
    pygame.time.delay(1500)
    game()

def show_cards(screen, deck):
    for card in deck.stack:
        screen.blit(card.back_image, (100, 220))

def create_labels(playerscore, dealerscore, screen):
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    player_label = font.render(f"Your Hand:", True, (255, 255, 255))
    dealer_label = font.render(f"Dealer's Hand:", True, (255, 255, 255))
    p_score_label = font.render(f"{playerscore}", True, (255, 255, 255))
    d_score_label = font.render(f"{dealerscore}", True, (255, 255, 255))
    chipcount = font.render(f"{playerchips}", True, (255, 255, 255))
    screen.blit(player_label, (10, 500))
    screen.blit(dealer_label, (10, 10))
    screen.blit(p_score_label, (70, 530))
    screen.blit(d_score_label, (70, 40))
    screen.blit(chipcount, (48, 580))
    pygame.display.update()

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
        screen.blit(card.back_image, (50, 260))
        # Update the x difference
        x_difference = target_position[0] - card.rect.x

        pygame.draw.rect(screen, (139, 0, 0), card.rect)
        # Draw the card at its new x position
        screen.blit(card.front_image, card.rect)

        # Control the frame rate for smooth animation
        clock.tick(60)

        pygame.display.update()

    # Now handle vertical movement
    while abs(y_difference) > speed:
        screen.blit(card.back_image, (50, 260))
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

    screen.blit(onehundred_text, (520, 645))
    screen.blit(twentyfive_text, (228, 645))
    screen.blit(fifty_text, (380, 645))
    screen.blit(fivehundred_text, (673, 645))
    screen.blit(five_text, (90, 645))
    pygame.display.flip()

    return fivehundred_button, onehundred_button, fifty_button, twentyfive_button, five_button


def create_buttons(screen):
    font = pygame.font.Font(None, 36)

    hit_button = pygame.Rect(500, 630, 80, 50)
    stand_button = pygame.Rect(250, 630, 80, 50)

    global button_list
    button_list = [hit_button, stand_button]
    pygame.draw.rect(screen, (0, 0, 0), hit_button)
    pygame.draw.rect(screen, (0, 0, 0), stand_button)


    hit_text = font.render("Hit", True, (255, 255, 255))
    stand_text = font.render("Stand", True, (255, 255, 255))

    screen.blit(hit_text, (525, 645))
    screen.blit(stand_text, (255, 645))

    pygame.display.flip()

    return hit_button, stand_button


def handle_hit(player, dealer, deck, screen):
    hitcount = 0
    if len(deck.stack) > 0:
        # Take the top card from the deck
        new_card = deck.stack.pop(0)
        # Add the new card to the player's hand
        player.append(new_card)
        print('HIT! New card dealt to player.')
        print(player)
        hitcount += 1



def handle_stand(dealer, player, deck, screen):
    # Dealer's turn

    dealer_score = calculate_scores(dealer)
    player_score = calculate_scores(player)

    while dealer_score < 17:
        if len(deck.stack) > 0:
            # Draw a card for the dealer
            new_card = deck.stack.pop(0)
            dealer.append(new_card)
            # Animate the card being dealt to the dealer
            dealer_score = calculate_scores(dealer)
            pygame.draw.rect(screen, (139, 0, 0), pygame.Rect(10, 500, 120, 36))
            pygame.draw.rect(screen, (139, 0, 0), pygame.Rect(10, 10, 200, 36))
            pygame.draw.rect(screen, (139, 0, 0), pygame.Rect(70, 530, 50, 36))
            pygame.draw.rect(screen, (139, 0, 0), pygame.Rect(70, 40, 50, 36))
            create_labels(player_score, dealer_score, screen)
            deal_cards(screen, new_card, (150 + (len(dealer) - 1) * 100, 50), speed=10)
            if dealer_score > player_score:
                break
    # Check the game outcome
    if dealer_score > 21:
        # Dealer busted, player wins
        dealer_busted_message(screen)

    elif dealer_score > player_score:
        # Dealer wins
        player_loses(screen)
    elif dealer_score < player_score:
        # Player wins
        player_wins(screen)

    elif dealer_score == player_score:
        push_message(screen)









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


def calculate_dealer_score(dealer, dealers_card_face_down):
    total_score = 0
    ace_count = 0

    # Iterate through dealer's cards
    for i, card in enumerate(dealer):
        # If the card is facedown, skip it if dealers_card_face_down is True
        if i == 1 and dealers_card_face_down:
            continue

        # Add the card's value to the total score
        if card.value == 'Ace':
            ace_count += 1
            total_score += 11
        elif card.value in ['King', 'Queen', 'Jack']:
            total_score += 10
        else:
            total_score += int(card.value)

    # Adjust the score if there are any Aces and the total score is greater than 21
    while ace_count > 0 and total_score > 21:
        total_score -= 10
        ace_count -= 1

    return total_score


def update_dealer_cards(dealer, screen, dealers_card_face_down):
    # Iterate through dealer's cards
    for i, card in enumerate(dealer):
        if i == 1:
            # Display front image if card should be face-up
            if not dealers_card_face_down:
                screen.blit(card.front_image, (150 + (i * 100), 50))
            # Display back image if card should be face-down
            else:
                screen.blit(card.back_image, (150 + (i * 100), 50))
        else:
            # Display front image for all other cards
            screen.blit(card.front_image, (150 + (i * 100), 50))


def game():
    import pygame
    global current_stage
    global playerchips
    global playerbet
    global player
    global dealer
    global dealers_card_face_down

    # Constants for game stages
    stage_bet = 1
    stage_play = 2


    # Initialize game state
    playerchips = 1000
    playerbet = 0
    player = []
    dealer = []
    screen, clock = init_pygame()
    running = True
    deck = Deck()
    deck.shuffle()
    for card in deck.stack:
        card.rect.topleft = (100, 220)

    # Create buttons for betting
    five_button, twentyfive_button, fifty_button, onehundred_button, fivehundred_button = create_bet_buttons(screen)
    hit_button, stand_button = create_buttons(screen)

    # Set initial game stage
    current_stage = stage_bet
    create_bet_buttons(screen)
    # Game loop
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle bet phase
                if current_stage == stage_bet:
                    create_bet_buttons(screen)
                    # Handle bet button clicks
                    bet_amount = None
                    if five_button.collidepoint(event.pos):
                        bet_amount = 5
                    elif twentyfive_button.collidepoint(event.pos):
                        bet_amount = 25
                    elif fifty_button.collidepoint(event.pos):
                        bet_amount = 50
                    elif onehundred_button.collidepoint(event.pos):
                        bet_amount = 100
                    elif fivehundred_button.collidepoint(event.pos):
                        bet_amount = 500

                    # If a valid bet amount is chosen
                    if bet_amount is not None and bet_amount <= playerchips:
                        playerbet = bet_amount
                        playerchips -= bet_amount

                        # Transition to play phase and deal initial cards
                        current_stage = stage_play
                        player.append(deck.stack.pop(0))
                        dealer.append(deck.stack.pop(0))
                        player.append(deck.stack.pop(0))
                        dealer.append(deck.stack.pop(0))

                        dealers_card_face_down = True

                # Handle play phase
                elif current_stage == stage_play:
                    if hit_button.collidepoint(event.pos):
                        handle_hit(player, dealer, deck, screen)
                        pygame.display.update()
                    elif stand_button.collidepoint(event.pos):
                        dealers_card_face_down = False
                        update_dealer_cards(dealer, screen, dealers_card_face_down)
                        handle_stand(dealer, player, deck, screen)
                        pygame.display.update()

        # Clear the screen
        screen.fill((139, 0, 0))
        playerscore = calculate_scores(player)
        dealerscore = calculate_dealer_score(dealer, dealers_card_face_down)
        create_labels(playerscore, dealerscore, screen)

        # Displaying the player's and dealer's cards in the play phase
        if current_stage == stage_play:
            create_buttons(screen)
            # Deal and animate cards to the player and dealer
            for i, card in enumerate(player):
                screen.blit(card.back_image, (50, 260))
                deal_cards(screen, card, (180 + (i * 100), 485), speed=10)

            for i, card in enumerate(dealer):
                if i == 1 and dealers_card_face_down:
                    screen.blit(card.back_image, (180 + (i * 100), 50))
                    #deal_cards(screen, card.back_image, (150 + (i * 100), 50), speed=10)
                else:
                    deal_cards(screen, card, (180 + (i * 100), 50), speed=10)
        # Redraw game elements based on the current stage


            create_buttons(screen)
            player_score = calculate_scores(player)
            dealer_score = calculate_dealer_score(dealer, dealers_card_face_down)
            if (dealer_score > 21) and (player_score <= 21):
                dealer_busted_message(screen)
            elif (dealer_score == 21) and (player_score < 21):
                dealer_blackjack(screen)
            elif (playerscore == 21) and (dealerscore < 21):
                player_blackjack(screen)
                playerchips = playerchips + (2 * playerbet)
            elif playerscore > 21:
                player_busted_message(screen)
            elif player_score == dealer_score:
                push_message(screen)
                playerchips = playerchips + playerbet
        elif current_stage == stage_bet:
            # Create and display bet buttons
            create_bet_buttons(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Clean up and exit
    pygame.quit()
# Run the main function to start the game loop
if __name__ == '__main__':
    game()

