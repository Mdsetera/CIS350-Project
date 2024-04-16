import pygame
import sys


def start_screen() -> int: #0 for texas holdem, 1 for blackjack
    pygame.init()

    # Set up screen
    screen = pygame.display.set_mode((800, 620))
    pygame.display.set_caption("Texas Hold'Em")
    font = pygame.font.Font(None, 36)

    # Set up buttons
    start_button = pygame.Rect(300, 400, 200, 50)
    blackjack_button = pygame.Rect(300, 460, 200, 50)
    quit_button = pygame.Rect(300, 520, 200, 50)

    #Set up start screen photo
    start_image = pygame.image.load('Images/startscreen.png')
    start_image = pygame.transform.scale(start_image, (300, 300))
    image_rect = start_image.get_rect(center=(400, 200))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  0# Starts the game
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif blackjack_button.collidepoint(event.pos):
                    return 1 #starts blackjack game

        # Draw buttons and text
        screen.fill((0, 128, 0))
        pygame.draw.rect(screen, (0, 0, 0), start_button)
        pygame.draw.rect(screen, (0, 0, 0), quit_button)
        pygame.draw.rect(screen, (0, 0, 0), blackjack_button)

        start_text = font.render("Start Game", True, (255, 255, 255))
        blackjack_text = font.render("BlackJack Mode", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        created_by_text = font.render("Created By: Mitchell Setera, Austin Jackson, & Caleb Taylor",
                                      True, (0, 0, 0))

        screen.blit(start_text, (335, 415))
        screen.blit(quit_text, (370, 535))
        screen.blit(blackjack_text, (305, 475))
        screen.blit(start_image, image_rect)
        screen.blit(created_by_text, (50, 580))
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()