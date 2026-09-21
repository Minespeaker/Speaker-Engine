name = input("Name: ")

import os

with open(f"{name}.py", "w", encoding="utf-8") as f:
    f.write(f"import pygame\nfrom pygame import freetype\npygame.init()\nfreetype.init()\n\nsw, sh = 500, 500\nscreen = pygame.display.set_mode((sw, sh))\npygame.display.set_caption(\"{name}\")\n\nfont = [freetype.SysFont(\"Arial\", s) for s in range (250)]\ncol = [(c, c, c) for c in range (256)]\n\nclock = pygame.time.Clock()\n\nrun = True\nwhile run:\n\tscreen.fill(col[0])\n\tfor e in pygame.event.get():\n\t\tif e.type == pygame.QUIT:\n\t\t\tpygame.quit()\n\t\t\texit()\n\n\tpygame.display.update()\n\tclock.tick(60)")
f.close()