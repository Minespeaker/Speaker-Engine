import pygame
import time
from math import *
pygame.init()

sw, sh = 1080, 720
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("3dCircle")

col = [(c, c, c) for c in range (256)]

clock = pygame.time.Clock()

def renderAtLatLong(surf, lat, long, cull=False):
    """
    Test
    
    :surf: Pygame surface to be blitted onto the surface
    :lat: The latitude to render at
    :long: The longitude to render at
    """
    
    global screen
    x, y = 0, 0
    
    lat = lat%360
    long = long%360
    
    p = True
    if 270 > lat > 90: p = False
    if 270 > long > 90: p = False
    
    # lat is in degrees so convert to radians
    latrad = lat/360
    longrad = long/360
    latrad *= 2*pi
    longrad *= 2*pi
	
    x = sin(longrad)*cos(latrad)*200
    y = sin(latrad)*200

    if p:
        dx, dy = surf.get_size()
        screen.blit(surf, ((sw//2)+x-(dx/2), (sh//2)+y-(dy/2)))

earthdaymap = pygame.image.load("map.jpg")
edx, edy = earthdaymap.get_size()

earthnightmap = pygame.image.load("mapNight.jpg")
enx, eny = earthnightmap.get_size()

earthday = [[earthdaymap.get_at((round((x/361)*edx), round((y/361)*edy))) for x in range (360)] for y in range (360)]
earthnight = [[earthnightmap.get_at((round((x/361)*enx), round((y/361)*eny))) for x in range (360)] for y in range (360)]

def getearthattime(day, night):
    t = time.gmtime()
    hour = t[3]+2.25
    mins = t[4]
    secs = t[5]
    
    secsTotal = secs+(mins*60)+(hour*3600)
    perOfDay = secsTotal/(60*60*24)
    perofEarth = round(-perOfDay*360)
    
    earthmap = day
    for row in range (360):
        for column in range (180):
            earthmap[row][(perofEarth+column)%360] = night[row][(perofEarth+column)%360]
    return earthmap

t = 0

run = True

clong = 0

l, r = False, False

tmp = pygame.Surface((4, 4))

while run:
    t += 1
    screen.fill(col[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                l = True
            if event.key == pygame.K_RIGHT:
                r = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                l = False
            if event.key == pygame.K_RIGHT:
                r = False
                
    if l:
        clong += 5
    if r:
        clong -= 5
            

    pygame.draw.circle(screen, col[64], (sw//2, sh//2), (200))

    earthmap = getearthattime(earthday, earthnight)

    for lat, x in enumerate (earthmap):
        for long, y in enumerate (x):
            tmp.fill(y)
            nlat = 300*(((lat*1)/edy)-0.3)
            nlong = (long*1)+clong
            renderAtLatLong(tmp, nlat, nlong, True)

    pygame.display.update()
    clock.tick(60)