import pygame
import sys


def start_screen():
    pygame.init()

    # Set up screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Texas Hold'Em")
    font = pygame.font.Font(None, 36)

    # Set up buttons
    start_button = pygame.Rect(300, 400, 200, 50)
    quit_button = pygame.Rect(300, 500, 200, 50)

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
                    return  # Starts the game
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw buttons and text
        screen.fill((0, 128, 0))
        pygame.draw.rect(screen, (0, 0, 0), start_button)
        pygame.draw.rect(screen, (0, 0, 0), quit_button)

        start_text = font.render("Start Game", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        created_by_text = font.render("Created By: Mitchell Setera, Austin Jackson, & Caleb Taylor",
                                      True, (0, 0, 0))

        screen.blit(start_text, (335, 415))
        screen.blit(quit_text, (370, 515))
        screen.blit(start_image, image_rect)
        screen.blit(created_by_text, (50, 570))
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()