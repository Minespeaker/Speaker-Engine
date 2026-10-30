import pygame
pygame.init()

col = [(c, c, c) for c in range (256)]

sw, sh = 500, 500
screen = pygame.display.set_mode((sw, sh))


clock = pygame.time.Clock()
grid = [[1, 1, 1]]

def conway():
    global grid
    eu = False
    ed = False
    er = False
    el = False
    
    if 1 in grid[0]:
        el = True
    if 1 in grid[-1]:
        er = True
    if 1 in [grid[i][0] for i in range (len(grid))]:
        eu = True
    if 1 in [grid[i][-1] for i in range (len(grid))]:
        ed = True
        
    if eu:
        for i in range (len(grid)):
            grid[i].insert(0, 0)
    if ed:
        for i in range (len(grid)):
            grid[i].append(0)
            
    if er:
        grid.append([0 for _ in range (len(grid[0]))])
    if el:
        grid.insert(0, [0 for _ in range (len(grid[0]))])
        
    new = grid
    
    for x in range (len(grid)-2):
        for y in range (len(grid[0])-2):
            n = 0
            
            u = y != 0
            d = y != len(grid[0])

            l = x != 0
            r = x != len(grid)
            
            if u:
                if l:
                    if grid[x-1][y-1] == 1: n += 1
                if grid[x+0][y-1] == 1: n += 1
                if r:
                    if grid[x+1][y-1] == 1: n += 1
            if grid[x+1][y+0] == 1: n += 1
            if d:
                if l:
                    if grid[x+1][y+1] == 1: n += 1
                if grid[x+0][y+1] == 1: n += 1
                if r:
                    if grid[x-1][y+1] == 1: n += 1
            if grid[x-1][y+0] == 1: n += 1
            
            if grid[x][y] == 0:
                if n == 3:
                    new[x][y] = 1
                else:
                    new[x][y] = 0
            else:
                if n in (2, 3):
                    new[x][y] = 1
                else:
                    new[x][y] = 0
                    
    grid = new

run = True
while run:
    screen.fill(col[0])
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
            
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            size = sw//len(grid)
            if grid[x][y] == 1:
                pygame.draw.rect(screen, col[255], (x*size, y*size, size, size))
            
    pygame.display.update()
    clock.tick(10)
    conway()
    print(grid)