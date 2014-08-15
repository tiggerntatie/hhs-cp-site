import pygame
from pygame.locals import *

pygame.init()
displaysurface = pygame.display.set_mode((600,200))
pygame.display.set_caption('Hello World!')
done = False
while not done: # main game loop
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True