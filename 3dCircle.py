import pygame
from pygame import freetype
from math import *
pygame.init()
freetype.init()

sw, sh = 500, 500
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("3dCircle")

font = [freetype.SysFont("Arial", s) for s in range (250)]
col = [(c, c, c) for c in range (256)]

clock = pygame.time.Clock()

def renderAtLatLong(surf, lat, long):
    """
    Test
    
    :surf: Pygame surface to be blitted onto the surface
    :lat: The latitude to render at
    :long: The longitude to render at
    """

run = True
while run:
	screen.fill(col[0])
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	pygame.draw.circle(screen, col[64], (sw//2, sh//2), (200))

	pygame.display.update()
	clock.tick(60)