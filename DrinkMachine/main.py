import pygame
from pygame import freetype
import math
import random

pygame.init()
freetype.init()

v = False

spamton = False

col = [(c, c, c) for c in range (256)]
font = [freetype.SysFont("Arial", s) for s in range (200)]

clock = pygame.time.Clock()

sw = 1366
sh = 768

if v:
    sw, sh = sh, sw

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("AI PLACEHOLDER NAME")

run = True

colour = (0, 0, 255)

l1 = 0
l2 = 0

blink = 0
eye = 120

p = 10

r = False

height = 400

change = 1

tpx = 0
tpy = 0
px = 0
py = 0

av = False

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                tpx = 0
                tpy = 0
                av = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                eye = 120
                av = False
            
    screen.fill(col[0])
            
    for x in range (round(sw*0.75)):
        screen.set_at(
                      (x+(sw//8), (sh*(0.6 if v else 0.8))+(math.sin((x/100)+(l1/10))*p)+(math.sin((x/53)+(l2/10))*p)),
                      (0, 0, min(max(750-abs((sw//2)-x), 0), 255))
                      )

    blink -= 1
    eye -= 1
    
    if blink <= 0:
        height -= change
        change *= 1.25 if change > 0 else 0.75
        if height <= 0:
            change = -change
        if height >= 400:
            height = 400
            change = 1
            blink = random.randint(200, 600)
            
    if eye <= 0 and not av:
        tpx = random.randint(-(sw//10)+50, (sw//10)-50)
        tpy = random.randint(-180, 180)
        eye = random.randint(45, 200)
    
    if av:
        p = max((p+1)**0.9, 0)-1
    else:
        p = min((p+1.1)**(1/0.9), 11)-1
        
    px += (tpx-px)//2
    py += (tpy-py)//2
    
    pygame.draw.rect(screen, colour, (sw*0.2, (200 if v else 100)+math.sin(l1)+(400-height), sw*0.2, max(height+math.sin(l1)*2, 0)), 0, 50)
    pygame.draw.rect(screen, colour, (sw*0.6, (200 if v else 100)+math.sin(l2)+(400-height), sw*0.2, max(height+math.sin(l2)*2, 0)), 0, 50)
    
    pygame.draw.circle(screen, (255, 174, 201) if spamton else (0, 255, 255), ((sw*0.3)+px, (400 if v else 300)+py), 20)
    pygame.draw.circle(screen, (255, 241, 0) if spamton else (0, 255, 255), ((sw*0.7)+px, (400 if v else 300)+py), 20)

    pygame.draw.circle(screen, (255, 241, 0) if spamton else (255, 255, 255), ((sw*0.3)+(px*1.05), (400 if v else 300)+(py*1.05)), 5)
    pygame.draw.circle(screen, (255, 174, 201) if spamton else (255, 255, 255), ((sw*0.7)+(px*1.05), (400 if v else 300)+(py*1.05)), 5)
    
    pygame.draw.rect(screen, col[0], (sw*0.2, (200 if v else 100)+math.sin(l1), sw*0.2, 400-height))
    pygame.draw.rect(screen, col[0], (sw*0.6, (200 if v else 100)+math.sin(l2), sw*0.2, 400-height))
    
    
    pygame.display.update()
    clock.tick(30)
    
    l1 += 0.25
    l2 += 0.3