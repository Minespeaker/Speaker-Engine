
import pygame; from pygame import freetype
display = pygame
fonts = freetype
display.init(); fonts.init()
font = [fonts.SysFont('Arial', s) for s in range (250)]
col = [(c, c, c) for c in range (256)]
screen = display.display.set_mode((500, 500))
display.display.set_caption('game1')
clock = pygame.time.Clock()
FRAME = -1
run = True
while run:
	key = None
	text = ''
	for event in display.event.get():
		if event.type == display.QUIT:
			run = False
		elif event.type == display.KEYDOWN:
			key = event.key
		elif event.type == display.TEXTINPUT:
			text = event.text
	mx, my = display.mouse.get_pos()
	mc = display.mouse.get_pressed()
	screen.fill(col[0])

	

	display.display.update(); clock.tick(60)
	FRAME += 1