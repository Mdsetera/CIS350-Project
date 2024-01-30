import pygame
from game_model import *


class GUI:
    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    clock = pygame.time.Clock()

    cards = [
        Card(1, Suit.CLUBS, "Images/cardClubsA.png"),
        Card(2, Suit.CLUBS, "Images/cardClubs2.png"),
        Card(3, Suit.CLUBS, "Images/cardClubs3.png"),
        Card(4, Suit.CLUBS, "Images/cardClubs4.png"),
        Card(5, Suit.CLUBS, "Images/cardClubs5.png"),
        Card(6, Suit.CLUBS, "Images/cardClubs6.png"),
        Card(7, Suit.CLUBS, "Images/cardClubs7.png"),
        Card(8, Suit.CLUBS, "Images/cardClubs8.png"),
        Card(9, Suit.CLUBS, "Images/cardClubs9.png"),
        Card(10, Suit.CLUBS, "Images/cardClubs10.png"),
        Card(10, Suit.CLUBS, "Images/cardClubsJ.png"),
        Card(10, Suit.CLUBS, "Images/cardClubsQ.png"),
        Card(10, Suit.CLUBS, "Images/cardClubsK.png"),
        Card(1, Suit.SPADES, "Images/cardSpadesA.png"),
        Card(2, Suit.SPADES, "Images/cardSpades2.png"),
        Card(3, Suit.SPADES, "Images/cardSpades3.png"),
        Card(4, Suit.SPADES, "Images/cardSpades4.png"),
        Card(5, Suit.SPADES, "Images/cardSpades5.png"),
        Card(6, Suit.SPADES, "Images/cardSpades6.png"),
        Card(7, Suit.SPADES, "Images/cardSpades7.png"),
        Card(8, Suit.SPADES, "Images/cardSpades8.png"),
        Card(9, Suit.SPADES, "Images/cardSpades9.png"),
        Card(10, Suit.SPADES, "Images/cardSpades10.png"),
        Card(10, Suit.SPADES, "Images/cardSpadesJ.png"),
        Card(10, Suit.SPADES, "Images/cardSpadesQ.png"),
        Card(10, Suit.SPADES, "Images/cardSpadesK.png"),
        Card(1, Suit.HEARTS, "Images/cardHeartsA.png"),
        Card(2, Suit.HEARTS, "Images/cardHearts2.png"),
        Card(3, Suit.HEARTS, "Images/cardHearts3.png"),
        Card(4, Suit.HEARTS, "Images/cardHearts4.png"),
        Card(5, Suit.HEARTS, "Images/cardHearts5.png"),
        Card(6, Suit.HEARTS, "Images/cardHearts6.png"),
        Card(7, Suit.HEARTS, "Images/cardHearts7.png"),
        Card(8, Suit.HEARTS, "Images/cardHearts8.png"),
        Card(9, Suit.HEARTS, "Images/cardHearts9.png"),
        Card(10, Suit.HEARTS, "Images/cardHearts10.png"),
        Card(10, Suit.HEARTS, "Images/cardHeartsJ.png"),
        Card(10, Suit.HEARTS, "Images/cardHeartsQ.png"),
        Card(10, Suit.HEARTS, "Images/cardHeartsK.png"),
        Card(1, Suit.DIAMONDS, "Images/cardDiamondsA.png"),
        Card(2, Suit.DIAMONDS, "Images/cardDiamonds2.png"),
        Card(3, Suit.DIAMONDS, "Images/cardDiamonds3.png"),
        Card(4, Suit.DIAMONDS, "Images/cardDiamonds4.png"),
        Card(5, Suit.DIAMONDS, "Images/cardDiamonds5.png"),
        Card(6, Suit.DIAMONDS, "Images/cardDiamonds6.png"),
        Card(7, Suit.DIAMONDS, "Images/cardDiamonds7.png"),
        Card(8, Suit.DIAMONDS, "Images/cardDiamonds8.png"),
        Card(9, Suit.DIAMONDS, "Images/cardDiamonds9.png"),
        Card(10, Suit.DIAMONDS, "Images/cardDiamonds10.png"),
        Card(10, Suit.DIAMONDS, "Images/cardDiamondsJ.png"),
        Card(10, Suit.DIAMONDS, "Images/cardDiamondsQ.png"),
        Card(10, Suit.DIAMONDS, "Images/cardDiamondsK.png"),
    ]

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 128, 0))
        card_width = (1900 - 50) // 13 - 10
        card_height = (1000 - 150) // 4 - 10
        columns = 13
        rows = 4

        for row in range(rows):
            for col in range(columns):
                index = row * columns + col
                if index < len(cards):
                    card = cards[index]
                    card.rect.topleft = (50 + col * (card_width + 10), 150 + row * (card_height + 10))
                    screen.blit(card.front_image, card.rect.topleft)

        pygame.display.flip()
        clock.tick(60)

