import pygame
import copy
from pygame import freetype
from Classes.pyselect import pyselect

class text:
    def get_text_width(text, font):
    
        text = str(text)
        
        if not pygame.display.get_init():
            pygame.display.init()
        
        text_rect = font.get_rect(text)
        
        return(text_rect.width+8)
    
    def edit_str(char, instr, blinkpos):
    
        if blinkpos > len(instr):
            blinkpos = len(instr)
                
        inlst = list(instr)
        
        if char == "BACKSPACE":
            if blinkpos != 0:
                blinkpos -= 1
                try:
                    del inlst[blinkpos]
                except Exception:
                    # defensive: if deletion fails, ignore
                    pass
    
        elif char == "UP":
            blinkpos = 0
            
        elif char == "DOWN":
            blinkpos = len(inlst)
            
        elif char == "LEFT":
            if blinkpos != 0:
                blinkpos -= 1
            
        elif char == "RIGHT":
            if blinkpos != len(inlst):
                blinkpos += 1
        
        elif char == "CTRL LEFT":
            # Move cursor to the start of the previous word
            if blinkpos > 0:
                i = blinkpos - 1
                # skip any trailing whitespace to the left
                while i > 0 and inlst[i].isspace():
                    i -= 1
                # now move to the start of the word
                while i > 0 and not inlst[i-1].isspace():
                    i -= 1
                blinkpos = i
        
        elif char == "CTRL RIGHT":
            # Move cursor to the start of the next word
            L = len(inlst)
            i = blinkpos
            # skip any whitespace to the right
            while i < L and inlst[i].isspace():
                i += 1
            # skip the current word
            while i < L and not inlst[i].isspace():
                i += 1
            blinkpos = i

        elif char == "ESCAPE":
            pass
            
        elif char != "":
            s = str(char)
            for ch in s:
                inlst.insert(blinkpos, ch)
                blinkpos += 1
        return "".join(inlst), blinkpos

class editor:
    def __init__(self, scroll_multiplier=0.2, size=tuple, font=None):
        screen_x, screen_y = size
        self.font = font
        if font == None:
            self.font = freetype.SysFont("Arial", 24)
        self.code = ["" for _ in range (1)]
        self.bpp, self.bpl = 0, 0
        self.scrn = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
        self.screen_size_x, self.screen_size_y = screen_x, screen_y
        pygame.draw.rect(self.scrn, (128, 128, 128), (0, 0, screen_x, screen_y), 5, 5)
        self.font_size = font.size
        self.sm = scroll_multiplier/self.font_size
        self.scrnps, self.scrnspd = 0, 0
        self.px, self.py = 0, 0
        self.md = False
        self.pos = [None, None]

        self.copyoneline = None
    
    def code_update(self, cpressed, scroll=0):
        mx, my = pygame.mouse.get_pos()
        mc = pygame.mouse.get_pressed()
        self.scrnspd += scroll*self.sm
        self.scrnspd *= 0.8
        self.scrnps += self.scrnspd
        self.scrnps = min(self.scrnps, len(self.code)-1)
        self.scrnps = max(self.scrnps, 0)
        if cpressed == "DOWN":
            tmp = self.bpl
            self.bpl = min(self.bpl+1, len(self.code)-1)
            if tmp == self.bpl:
                self.bpp = len(self.code[self.blist(self.scrn.get_size())[0]])-1
        elif cpressed == "UP":
            tmp = self.bpl
            self.bpl = max(self.bpl-1, 0)
            if self.bpl == tmp:
                self.bpp = 0
        elif cpressed == "RETURN":
            self.bpl += 1
            self.code.insert(self.bpl, "")
        elif cpressed == "BACKSPACE" and self.bpp == 0:
            self.bpp = len(self.code[self.bpl-1])
            self.bpl -= 1
            self.code.pop(self.bpl+1)
            if self.bpl == -1:
                self.bpl += 1
            if self.code == []:
                self.code.append("")
        elif cpressed == "TAB":
            tmp = list(self.code[self.bpl])
            tmp.insert(self.bpp, "\t")
            self.code[self.bpl] = "".join(tmp)
            self.bpp += 1
        else:
            line = self.code[int(self.bpl)]
            line, self.bpp = text.edit_str(cpressed, line, self.bpp)
            self.code[int(self.bpl)] = line

        if mc[0] and not self.md:
            self.md = True
            self.mdx, self.mdy = mx, my
        if self.md and not mc[0]:
            self.md = False
            if abs(mx-self.mdx) > 3 or abs(my-self.mdy) > 3:
                self.pos[0] = list((self._get_pos_of_mouse(self.mdx, self.mdy)))
                self.pos[1] = list((self._get_pos_of_mouse(my, my)))
                if self.pos[0][0] == self.pos[1][0]:
                    tmp = self.code[self.pos[0][0]].split(None)
                    self.txtcopy = "".join(tmp[self.pos[0][1]:self.pos[1][1]])
                    self.copyoneline = True
            else:
                self.bpl ,self.bpp = self._get_pos_of_mouse(mx, my)
                self.pos = [[], []]
            
    def _get_pos_of_mouse(self, mx, my):
        mx -= self.px
        my -= self.py
        my += self.scrnps*self.font_size

        if mx > 0 and my > 0:
            tl = my/self.font_size
            b = 0
            if tl < len(self.code):

                line = self.code[self.bpl]
                bp = []
                for i in range (len(line)):
                    bp.append(abs(mx-(text.get_text_width("".join(list(line)[:i]), self.font))))
                bp.append(abs(mx-(text.get_text_width(line, self.font))))
                bv = -1
                for v, k in enumerate(bp):
                    if k < bv or bv == -1:
                        bv = k
                        b = v
                return int(tl), b
        return self.bpl, self.bpp

    def draw(self, screen, pos):
        self.scrn = pygame.Surface((self.screen_size_x, self.screen_size_y))
        self.scrn.fill((16, 16, 16))
        pygame.draw.rect(self.scrn, (128, 128, 128), (0, 0, self.screen_size_x, self.screen_size_y), 5, 5)
        self.px, self.py = pos
        self.px = round(self.px); self.py = round(self.py)
        pos = (self.px, self.py)
        for i in range (len(self.code)):
            line = copy.deepcopy(self.code[i])
            indent = line.count("\t")
            line = list(line)
            for _ in range (line.count("\t")):
                line.pop(line.index("\t"))
            line = "".join(line)
            pygame.draw.rect(self.scrn, (64, 64, 64), (0, round(((1+i)*self.font_size)-(self.scrnps*self.font_size)), round(self.scrn.get_width()-10), 1))
            if round(((i)*self.font_size)-(self.scrnps*self.font_size)) >= 0 and round(((i)*self.font_size)-(self.scrnps*self.font_size)) <= self.screen_size_y:
                self.font.render_to(self.scrn, (7+(indent*15), round(((i)*self.font_size)-(self.scrnps*self.font_size))+6), line, (192, 192, 192))
            if i == self.bpl:
                pygame.draw.rect(self.scrn, (255, 255, 255), (round((text.get_text_width(line[:self.bpp], self.font)))+(indent*15), round(((i)*self.font_size)-(self.scrnps*self.font_size)+6), 2, self.font_size-8))
            if self.copyoneline != None:
                if self.copyoneline:
                    pass
        screen.blit(self.scrn, pos)
