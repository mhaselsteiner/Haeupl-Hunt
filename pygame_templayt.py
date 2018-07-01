import pygame
import random

pygame.init()
pygame.mixer.init()  # initializes sound
WIDTH = 360
HEIGHT = 480
FPS = 30  #frames per second
#define colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

#Game loop
running = True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #process input
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running = False
#update
    all_sprites.update()
    #draw
    all_sprites.draw(screen)
    screen.fill(BLACK)
    #after drwing flip display
    pygame.display.flip()  # shows new screen graphics
