import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
GRID_SIZE = 4  
FPS = 30

WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

CARD_IMAGES = ["🍎", "🍌", "🍒", "🍍", "🍇", "🍉", "🍓", "🍊"]
CARD_IMAGES *= 2  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Matching Game")

class Card:
    def __init__(self, x, y, image, index):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.image = image  
        self.flipped = False
        self.matched = False
        self.index = index

    def draw(self, surface):
        if self.flipped or self.matched:
            font = pygame.font.Font(None, 48)
            text = font.render(self.image, True, WHITE)
            surface.blit(text, self.rect.center)
        else:
            pygame.draw.rect(surface, GREEN, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 5)  

def init_game():
    cards = []
    positions = []
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CARD_WIDTH + 10) + 50
            y = row * (CARD_HEIGHT + 10) + 50
            positions.append((x, y))

    random.shuffle(CARD_IMAGES)  
    for i, (x, y) in enumerate(positions):
        card = Card(x, y, CARD_IMAGES[i], i)
        cards.append(card)
    
    return cards

def game_loop():
    cards = init_game()
    flipped_cards = []
    matched_cards = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and len(flipped_cards) < 2:
                mouse_x, mouse_y = event.pos
                for card in cards:
                    if card.rect.collidepoint(mouse_x, mouse_y) and not card.flipped and not card.matched:
                        card.flipped = True
                        flipped_cards.append(card)

        if len(flipped_cards) == 2:
            card1, card2 = flipped_cards
            if card1.image == card2.image:
                card1.matched = True
                card2.matched = True
                matched_cards += 2
            else:
                pygame.time.wait(500) 
                card1.flipped = False
                card2.flipped = False
            flipped_cards = []

        for card in cards:
            card.draw(screen)

        if matched_cards == len(cards):
            font = pygame.font.Font(None, 36)
            win_text = font.render("You Win!", True, BLUE)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
