import pygame, os, math, time, pyperclip, sys, subprocess, copy, multiprocessing, platform
from pygame import freetype
from modulefinder import ModuleFinder

OS = platform.system()

osvar = {"Windows": "Microsoft windows", "Linux": "Linux"}

OS = osvar[OS]

if OS == "Linux":
    OS = f"{OS}: {platform.freedesktop_os_release()["NAME"]} {platform.freedesktop_os_release()["VERSION_CODENAME"]} {platform.freedesktop_os_release()["VERSION"]}"
 
print(f"Detected OS Environment: {OS}")

time.sleep(1)

sep = "\\" if "Windows" in OS else "/"

debug = True
skip = True

tmp = os.path.dirname(__file__)
tmp = tmp.split(sep)
FILE_PATH = sep.join(tmp)+sep
print(FILE_PATH)
sys.path[0] = (FILE_PATH)

if not os.path.exists(os.path.join(FILE_PATH, "GAMES")):
    os.mkdir(os.path.join(FILE_PATH, "GAMES"))
    for i in os.listdir(os.path.join(FILE_PATH, "Quickaccess")):
        os.remove(os.path.join(FILE_PATH, "Quickaccess", i))

file_type = ".sngf"

def dprint(*args):
    global debug
    try:
        if debug:
            print(args)
    except NameError:
        debug = False

class execute:
    def __init__(self, screen, base_vars):
        """
        Initialise the Container
        
        :param self: The Container
        :param screen: A Tuple of the size of the Screen, leave as empty Tuple for no screen
        :param base_vars: Variables that are existant by default
        """
        self.container = {} if base_vars == None else dict(base_vars)
        self.frame = 0
        if screen != ():
            self.add_class("pygame", "display", "")
            self.add_class("freetype", "fonts", "pygame")
            self.run_code("display.init()")
            self.run_code("fonts.init()")
            self.run_code(f"screen = display.Surface({screen})\n")
            self.run_code(f"font = [fonts.SysFont('Arial', s) for s in range (500)]")

    def add_class(self, classv, targ_class_name, parclass):
        if isinstance(targ_class_name, str):
            if parclass != "":
                exec(f"from {parclass} import {classv} as {targ_class_name}", self.container, self.container)
            else:
                exec(f"import {classv} as {targ_class_name}", self.container, self.container)
        else:
            self.container[targ_class_name] = classv

    def set_screen_size(self, size):
        self.run_code(f"screen = display.Surface({size})\n")

    def run_code(self, code):
        tmp = self.container
        try:
            exec(code, self.container, self.container)
            return ""
        except Exception as e:
            self.container = tmp
            return str(e)

    def run_display(self, code):
        prev_frame = self.container
        self.container["FRAME"] = self.frame
        try:
            exec(code, self.container, self.container)
        except Exception as e:
            self.container = prev_frame
            return self.container["screen"], str(e)
        self.frame += 1
        self._loop = code
        return self.container["screen"], ""
        
    def get_var(self, var=str):
        return self.container[var]
    
    def getout(self, code):
        if isinstance(code, str):
            code = [code]
        import copy
        tmp = copy.deepcopy(self.container)
        code[-1] = "out = "+str(code[-1])
        exec("\n".join(code), tmp, tmp)
        return tmp["out"]
    
    def get_code():
        out = []
        
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
        elif cpressed == "ENTER":
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
            dprint(line)
            pygame.draw.rect(self.scrn, (64, 64, 64), (0, round(((1+i)*self.font_size)-(self.scrnps*self.font_size)), round(self.scrn.get_width()-10), 1))
            if round(((i)*self.font_size)-(self.scrnps*self.font_size)) >= 0 and round(((i)*self.font_size)-(self.scrnps*self.font_size)) <= self.screen_size_y:
                self.font.render_to(self.scrn, (7+(indent*15), round(((i)*self.font_size)-(self.scrnps*self.font_size))+6), line, (192, 192, 192))
            if i == self.bpl:
                pygame.draw.rect(self.scrn, (255, 255, 255), (round((text.get_text_width(line[:self.bpp], self.font)))+(indent*15), round(((i)*self.font_size)-(self.scrnps*self.font_size)+6), 2, self.font_size-8))
            if self.copyoneline != None:
                if self.copyoneline:
                    pass
        screen.blit(self.scrn, pos)

class pyselect:
    class button:
        def __init__(
            self,
            text,
            font,
            x,
            y,
            width,
            height,
            butt_col,
            select_col,
            text_col,
            corner_round=0
        ):
            self.text = text
            self.font = font
            self.x, self.y = x, y
            self.w, self.h = width, height
            self.rect = pygame.Rect(x, y, width, height)

            self.butt_col = butt_col
            self.select_col = select_col
            self.text_col = text_col
            self.corner_round = corner_round

            self.clicked = False
            self._was_pressed = False

            self.hover = False

        def draw(self, screen):
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            hover = self.rect.collidepoint(mouse_pos)
            color = self.select_col if hover else self.butt_col

            # Click detection (edge-triggered)
            if hover and mouse_pressed and not self._was_pressed:
                self.clicked = True
                self._was_pressed = True
            else:
                self.clicked = False

            if not mouse_pressed:
                self._was_pressed = False

            # Draw button
            if hover:
                self.hover = True
                pygame.draw.rect(
                    screen,
                    self.select_col,
                    self.rect.inflate(4, 4),
                    0,
                    self.corner_round
                )
            
            else:
                self.hover = False

            pygame.draw.rect(
                screen,
                self.butt_col,
                self.rect,
                0,
                self.corner_round
            )

            self._draw_text(screen)

        def _draw_text(self, screen):
            try:
                rendered = self.font.render(self.text, fgcolor=self.text_col)
            except TypeError:
                rendered = self.font.render(self.text, True, self.text_col)

            if isinstance(rendered, tuple):
                surface, rect = rendered
            else:
                surface = rendered
                rect = surface.get_rect()

            rect.center = self.rect.center
            screen.blit(surface, rect)

        def was_clicked(self):
            return self.clicked
        
        def hovering(self):
            return self.hover

    class dropdown:
        def __init__(
            self,
            options,
            font,
            x,
            y,
            width,
            height,
            butt_col=(64, 64, 64),
            select_col=(128, 128, 128),
            text_col=(255, 255, 255),
            hover_col=(16, 16, 16),
            current_select_col=(32, 32, 32),
            gap=0,
            corner_round=0,
            horizontal=False,
            both=False,
            start_option=None
        ):
            self.options = options
            self.font = font
            self.open = False
            self.selected = start_option if start_option != None else self.options[0]
            self.button_select = False
            self.csc = current_select_col
            self.gap = gap
            self.x, self.y = x, y
            
            self.btc, self.hvc = butt_col, hover_col

            self.main_button = pyselect.button(
                self.selected,
                font,
                x,
                y,
                width,
                height,
                butt_col,
                select_col,
                text_col,
                corner_round
            )

            self.gap = gap
            self.options = options
            self.horizontal = horizontal
            self.both = both
            self.width, self.height = width, height

            self.option_buttons = []
            self.option_index = []
            for i, text in enumerate(options):
                ox = x + ((gap * (i+1)) + (width * i) if horizontal or both else 0)
                oy = y + ((gap * (i+1)) + (height * i) if not horizontal or both else 0)
                self.option_index.append(text)
                self.option_buttons.append(
                    pyselect.button(
                        text,
                        font,
                        ox+(width if both or horizontal else 0),
                        oy+(height if both or not horizontal else 0),
                        width,
                        height,
                        butt_col,
                        select_col,
                        text_col,
                        corner_round
                    )
                )

        def draw(self, screen):
            self.main_button.text = self.selected
            self.main_button.butt_col = self.hvc if self.open else self.btc
            self.main_button.draw(screen)

            for i in range(len(self.options)):
                ox = self.x + ((self.gap * (i+1)) + (self.width * i) if self.horizontal or self.both else 0)
                oy = self.y + ((self.gap * (i+1)) + (self.height * i) if not self.horizontal or self.both else 0)
                self.option_buttons[i].x, self.option_buttons[i].y = ox+(self.width if self.both or self.horizontal else 0), oy+(self.height if self.both or not self.horizontal else 0)

            self.main_button.x, self.main_button.y = self.x, self.y

            if self.main_button.was_clicked():
                self.open = True
                self.button_select = True
                for i in range (len(self.option_buttons)):
                    self.option_buttons[i].butt_col = self.btc
                    
            self.option_buttons[self.option_index.index(self.selected)].butt_col = self.csc

            if not pygame.mouse.get_pressed()[0]:
                self.button_select = False

            if self.open and not self.button_select:
                for button in self.option_buttons:
                    button.draw(screen)
                    if button.was_clicked():
                        self.selected = button.text
                        self.open = False
                        return
                if pygame.mouse.get_pressed()[0]:
                    self.open = False

        def get_selected(self):
            return self.selected
        
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
        
        elif char == "WORD_LEFT":
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
        
        elif char == "WORD_RIGHT":
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



cpfl = None

ld = {"sx": 0, "sy": 0, "menu_open": False, "menu_slt": None, "rnm": False, "rnt": None}

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    # Hue
    if diff == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    # Saturation
    s = 0 if mx == 0 else diff / mx

    # Value
    v = mx

    return h, s, v

def recursive_scan(dir, q, file=None, _parent=True):
    global sep
    dprint(f"Filescan: Dir: {dir}, Sep: {sep}")
    name = dir.split(sep)[-1]
    if file == None:
        file = {name: ({}, _parent)}
    files, headunpack = file[name]
    filen = {}
    for folder in [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]:
        foldername = folder
        if folder in files:
            contents, unpack = files[folder]
        else:
            contents = {}
            unpack = False
        childdata = recursive_scan(os.path.join(dir, folder), q, {foldername: (contents, unpack)}, False)
        contents, _ = childdata[foldername]
        filen[folder] = contents, unpack
        dprint("Filescan: Folder")
    for file in [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]:
        filen[file] = loadbin(os.path.join(dir, file))
        dprint("Filescan: File")
    filen = {name: (filen, headunpack)}
    if _parent:
        q.put(filen)
    return filen

def loadbin(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()

    return(file_content)

def savebin(file_path, string):
    text_to_write = string
    norm_path = os.path.normpath(file_path)
    dirpath = os.path.dirname(norm_path)
    if dirpath:
        try:
            os.makedirs(dirpath, exist_ok=True)
        except Exception:
            pass
    try:
        with open(norm_path, "wb") as f:
            f.write(text_to_write)
    except FileExistsError:
        with open(norm_path, "wbx") as f:
            f.write(text_to_write)
    
def listfiles(foldername, files, txtin, size, scrn, off, mx, my, mc, _parent=True, path=[], ogox=None, ogoy=None):
    global ld, sep
    if _parent:
        path = []
    dprint(f"Listfiles: wakeup as {f"ChildProcess with Dir {f"{sep}".join(path)}{sep}{foldername}" if not _parent else "ParentProcess"}")
    pygame.init()
    freetype.init()
    dprint("Listfiles: PG+PGFT init pass")
    if txtin == "BACKSPACE":
        dprint("Listfiles: Bspace detect")
    ox, oy = off
    if ogox == None or ogoy == None:
        ogox, ogoy = ox, oy
    path.append(foldername)
    dprint(f"Listfiles: {path}")
    x, y = size
    _pos = 0
    linesize = 25
    indent = 25
    dprint(f"Listfiles: {x}, {y}")
    if x < 0: x = 0
    if y < 0: y = 0
    surf = pygame.Surface((x, y), pygame.SRCALPHA)
    txt = freetype.SysFont("Arial", linesize-2)
    scrnrect = pygame.Rect(ox, oy, x, y)
    hover = False
    
    scrnsz = scrn
    scrn = pygame.Surface(scrnsz, pygame.SRCALPHA)
    
    folders = set()

    if _parent:
        tmprect = pygame.Rect(ox, oy, x, linesize)
        if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
            pygame.draw.rect(scrn, (192, 192, 192, 128), tmprect)
            if mc[0]:
                dprint(files)
                files = {foldername: (list(files[foldername])[0], not list(files[foldername])[1])}
            if mc[2]:
                ld["menu_open"] = True
                ld["menu_slt"] = path
                ld["sx"], ld["sy"] = mx, my
    if _parent:
        if list(files[foldername])[1]:
            txt.render_to(surf, (0, 0), f"{foldername} ▾", (255, 255, 255))
        else:
            txt.render_to(surf, (0, 0), f"{foldername} ▸", (255, 255, 255))
    else:
        txt.render_to(surf, (0, 1), f"|-{foldername} ▾", (255, 255, 255))

    dprint("Listfiles: Full Init Pass")
    dprint(f"Listfiles: {files}")
    unpackedfiles, headunpack = files[foldername]
    dprint(f"Listfiles: {unpackedfiles}")
    if headunpack:
        for name, data in unpackedfiles.items():
            dprint(f"Listfiles: {name}, {data}")
            _pos += 1   
            if type(data) == tuple:
                contents, unpack = data
                dprint(f"Listfiles: {contents}")
                dprint(f"Listfiles: {unpack}")
                tmprect = pygame.Rect(-indent*(len(path)+1)+ox, _pos*linesize+oy, x+indent*(len(path)+1), linesize)
                if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
                    hover = True
                    hoverpos = _pos
                    if mc[0]:
                        unpack = not unpack
                        unpackedfiles[name] = contents, unpack
                        data = unpackedfiles[name]
                    if mc[2]:
                        ld["menu_open"] = True
                        ld["menu_slt"] = path
                        ld["menu_slt"].append(name)
                        ld["sx"], ld["sy"] = mx, my
                dprint(f"Listfiles: {data}")
                dprint(f"Listfiles: {contents}")
                dprint(f"Listfiles: {unpack}")
                if unpack:
                    dprint("Listfiles: Open folder")
                    childsurf, childfiles, childpos = listfiles(name, {name: data}, txtin, (x-indent, y-(_pos-linesize)), scrnsz, (ox+indent, oy+_pos*linesize), mx, my, mc, False, list(path), ogox, ogoy)
                    unpackedfiles[name] = childfiles, unpack
                    folders.add(childsurf)
                    for _ in range (childpos):
                        _pos += 1
                        txt.render_to(surf, (indent, _pos*linesize), "|", (255, 255, 255))
                else:
                    dprint("Listfiles: Comp folder")
                    txt.render_to(surf, (indent, _pos*linesize), f"|-{name} ▸", (255, 255, 255))


            else:
                dprint("Listfiles: File")
                tmprect = pygame.Rect(-indent*(len(path)+1)+ox, _pos*linesize+oy, x+indent*(len(path)+1), linesize)
                if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
                    hover = True
                    hoverpos = _pos
                    
                    if mc[2]:
                        ld["menu_open"] = True
                        ld["menu_slt"] = path
                        ld["menu_slt"].append(name)
                        ld["sx"], ld["sy"] = mx, my
                    
                txt.render_to(surf, (indent, _pos*linesize), f"|-{name}", (255, 255, 255))
    files = {foldername: (unpackedfiles, headunpack)}
    scrn.blit(surf, off)
    dprint(ld)
    dprint(path)
    menu = pygame.Rect(ld["sx"], ld["sy"], 120, 150)
    
    if menu.collidepoint(mx, my) and ld["menu_open"]:
        hover = False
    if mc[0] and not menu.collidepoint(mx, my):
        ld["sx"], ld["sy"] = 0, 0
        ld["menu_open"] = False
        ld["menu_slt"] = None
        ld["rnt"] = None
        ld["rnm"] = False
    if hover:
        selrect = pygame.Surface((x+indent*(len(path)+1), linesize), pygame.SRCALPHA)
        pygame.draw.rect(selrect, (192, 192, 192, 128), (0, 0, ox+x, linesize))
        scrn.blit(selrect, (ogox, oy+hoverpos*linesize))
    pygame.draw.rect(surf, ((0, 0, 0, 1)), (indent, ((_pos+1)*linesize)-(linesize*0.525), 12, linesize*0.525))
    
    for folder in folders:
        scrn.blit(folder, (0, -1))
        
    if ld["menu_slt"] != None:
        if ld["menu_slt"] == path or ld["menu_slt"][:-1] == path:
            txt2 = freetype.SysFont("Arial", 20)
            slc = ld["menu_slt"] == path
            slf = ld["menu_slt"][-1]
            bx, by = ld["sx"], ld["sy"]
            pygame.draw.rect(scrn, col[64], menu, 0, 5)
            ls = 25
            nfl = pygame.Rect(bx, by+5, list(menu.size)[0], 20)
            nfd = pygame.Rect(bx, by+5+ls, list(menu.size)[0], 20)
            rnm = pygame.Rect(bx, by+5+(ls*2), list(menu.size)[0], 20)
            dlt = pygame.Rect(bx, by+5+(ls*3), list(menu.size)[0], 20)
            cpy = pygame.Rect(bx, by+5+(ls*4), list(menu.size)[0], 20)
            pst = pygame.Rect(bx, by+5+(ls*5), list(menu.size)[0], 20)
                
            global cpfl
            
            if nfl.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], nfl)
            if nfd.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], nfd)
            if rnm.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], rnm)
                if mc[0] or ld["rnm"]:
                    if ld["rnm"]:
                        if txtin == "BACKSPACE":
                            ld["rnt"] = "".join(list(ld["rnt"])[:-1])
                            dprint("Listfiles: Bspace used")
                        elif txtin == "ENTER":
                            fd = loadbin(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                            savebin(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"][:-1]), ld["rnt"]), fd)
                            os.remove(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                            ld["menu_open"] = False
                            ld["menu_slt"] = None
                            ld["rnt"] = None
                            ld["rnm"] = False
                        else:
                            ld["rnt"] = f"{ld["rnt"]}{txtin}"
                    else:
                        ld["rnm"] = True
                        ld["rnt"] = ld["menu_slt"][-1]
            if dlt.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], dlt)
                if mc[0]:
                    os.remove(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                    ld["menu_open"] = False
                    ld["menu_slt"] = None
            if cpy.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], cpy)
                if mc[0]:
                    ld["menu_open"] = False
                    ld["menu_slt"] = None
                    ld["rnt"] = None
                    ld["rnm"] = False
                    if slc:
                        cpfl = slf, unpackedfiles
                    else:
                        cpfl = slf, list(unpackedfiles[slf])[0]
            if pst.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], pst)
            
            txt2.render_to(scrn, (bx+5, by+5), "New File", col[255])
            txt2.render_to(scrn, (bx+5, by+5+ls), "New Folder", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*2)), ld["rnt"] if ld["rnm"] else "Rename", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*3)), "Delete", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*4)), "Copy", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*5)), "Paste", col[255 if cpfl != None else 127])
            
    path = path[:-1]
    if _parent:
        dprint("Listfiles: Parent subpro fi")
        dprint("Listfiles: Return Success")
        return scrn, files
        
    else:
        dprint("Listfiles: Child subpro fi")
        dprint(files)
        return scrn, unpackedfiles, _pos

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        rp, gp, bp = c, x, 0
    elif 60 <= h < 120:
        rp, gp, bp = x, c, 0
    elif 120 <= h < 180:
        rp, gp, bp = 0, c, x
    elif 180 <= h < 240:
        rp, gp, bp = 0, x, c
    elif 240 <= h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x

    r = int((rp + m) * 255)
    g = int((gp + m) * 255)
    b = int((bp + m) * 255)

    return r, g, b

def convert_to_standalone_exe(script_path):
    """
    Converts a Python script into a standalone .exe file.
    Includes custom classes and modules automatically via PyInstaller's analysis.
    """
    if not os.path.exists(script_path):
        dprint(f"Error: The file '{script_path}' was not found.")
        return

    dprint(f"--- Starting Build Process for: {script_path} ---")
    
    script_path = "'"+script_path+"'"

    # Construct the PyInstaller command
    # --onefile: Create a single executable
    # --noconfirm: Replace existing output directories without asking
    # --clean: Clean PyInstaller cache before building

    import time


    command = [
        "pyinstaller",
        "--onefile",
        "--noconfirm",
        "--clean",
        script_path
    ]

    try:
        # Execute the command
        subprocess.check_call("pip install pyinstaller", shell=True)
        subprocess.check_call(" ".join(command), shell=True)
        dprint("BUILD SUCCESSFUL!")
        
    except subprocess.CalledProcessError as e:
        dprint(f"An error occurred during the build: {e}")
    except Exception as e:
        dprint(f"Unexpected error: {e}")
    
def estimate_build_time(script_path):
    finder = ModuleFinder()
    finder.run_script(script_path)
    
    # Count unique modules found
    num_modules = len(finder.modules)
    
    # Rough heuristic: 0.5 seconds per module + 10s overhead 
    # (Adjust '0.5' based on your specific machine's performance)
    base_overhead = 10 
    predicted_seconds = (num_modules * 0.5) + base_overhead
    
    return num_modules, predicted_seconds

def replace_str(full_string, sub_string):
    """
    Removes the first occurrence of sub_string from full_string.
    """
    if sub_string in full_string:
        return full_string.replace(sub_string, "", 1)
    return full_string

def sort(list, list2):
    list3 = []
    for i in range (len(list2)):
        list3.append(list2.index(min(list2)))
        list2[list3[-1]] = 99999999999
    list4 = [list[list3[i]] for i in range (len(list))]
    return(list4)

def warp(tfont, text, max_width):
    def text_width(s):
        return tfont.get_rect(s).width

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = word if current_line == "" else current_line + " " + word

        if text_width(test_line) <= max_width:
            current_line = test_line
        else:
            if text_width(word) > max_width:

                if current_line:
                    lines.append(current_line)
                    current_line = ""

                chunk = ""
                for char in word:
                    test_chunk = chunk + char
                    if text_width(test_chunk) <= max_width:
                        chunk = test_chunk
                    else:
                        lines.append(chunk)
                        chunk = char
                if chunk:
                    current_line = chunk

            else:
                lines.append(current_line)
                current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def compile_files():
    
        global loading, max_dist, sort_order, files, screen_width

        max_dist = 0

        files = get_files(FILE_PATH+"Quickaccess")
        if debug:
            dprint(len(files))
        if len(screen) == 1:
            screen.append([None])
        file_infos = [(os.stat(os.path.join(FILE_PATH+"Quickaccess", files[i]))) for i in range (len(files))]

        file_btime = [file_infos[i].st_ctime for i in range (len(file_infos))]

        file_etime = [file_infos[i].st_mtime for i in range (len(file_infos))]

        if sort_order == "az":
            files = alph_list(files)
        elif sort_order == "za":
            files = alph_list(files)
            files.reverse()
        elif sort_order == "bn":
            files = sort(files, file_btime)
            files.reverse()
        elif sort_order == "bo":
            files = sort(files, file_btime)
        elif sort_order == "en":
            files = sort(files, file_etime)
            files.reverse()
        elif sort_order == "eo":
            files = sort(files, file_etime)


        file_infos = [(os.stat(FILE_PATH+"Quickaccess"+sep+files[i])) for i in range (len(files))]

        file_btime = [file_infos[i].st_ctime for i in range (len(file_infos))]

        file_etime = [file_infos[i].st_mtime for i in range (len(file_infos))]



        for i in range (len(files)):
            if len(screen[1]) <= i:
                screen[1].append(None)

            screen[1][i] = pygame.Surface((screen_width, (i*225)+300), pygame.SRCALPHA)
            name = files[i]

            file_info = os.stat(FILE_PATH+"Quickaccess"+sep+name)
            file_size = file_info.st_size
            file = string_to_list(load(os.path.join(FILE_PATH+"Quickaccess", name)), "\nbreak\n")



            file = string_to_list(load(FILE_PATH+"Quickaccess"+sep+name), "\nbreak\n")
            file[1] = replace_str(file[1], "")

            if len(file) == 1:
                file.append("Failed to get")

            if file[1] == "":
                file[1] = "Failed to get"

            if debug:
                dprint(name)
                dprint(file)

            file_disc = file[0]

            disc = warp(font[18], file_disc, screen_width-100)
            if len(disc) >= 4:
                txt = list(disc[3])
                txt[-1], txt[-2], txt[-3] = ".", ".", "."
                disc = [disc[0], disc[1], disc[2], "".join(txt)]


                

            toobig = True

            file_size_meas = ["B", "KB", "MB", "GB", "TB"]

            file_meas = 0

            while toobig:
                if file_size >= 1024:
                    file_size /= 1024
                    file_meas += 1
                else:
                    toobig = False
                if file_meas == len(file_size_meas):
                    toobig = False
            
            file_size = round(file_size*10)/10
            if str(file_size).__contains__(".0"):
                file_size = int(file_size)

            name = replace_str(name, file_type)

            btime = file_btime[i]
            etime = file_etime[i]
            dprint(etime-btime)
            btime = time.ctime(btime)
            etime = time.ctime(etime)
            if etime == btime:
                etime = "Never"



            pygame.draw.rect(screen[1][i], col[40], (15, math.floor(((i+3)*25)+(i*200)), screen_width-50, 200), 0, 25)
            dprint(screen_width)
            font[40].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+20)), name, fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+65)), "Description:", fgcolor=col[255])
            if disc != []:
                for i2 in range (len(disc)):
                    font[14].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+((i2)*16)+85)), disc[i2], fgcolor=col[192])
            else:
                font[18].render_to(screen[1][i], (24, math.floor(((i+3)*25)+(i*200)+85)), "There is no description for this game", fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+150)), "Details:", fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+175)), "Size: "+str(file_size)+" "+file_size_meas[file_meas], fgcolor=col[255])
            font[18].render_to(screen[1][i], (250, math.floor(((i+3)*25)+(i*200)+150)), "Created: "+btime, fgcolor=col[255])
            font[18].render_to(screen[1][i], (252, math.floor(((i+3)*25)+(i*200)+175)), "Last Edited: "+etime, fgcolor=col[255])
            font[18].render_to(screen[1][i], (600, math.floor(((i+3)*25)+(i*200)+150)), "Type: "+replace_str(file[1], "\n"), fgcolor=col[255])

            max_dist = (((i+3)*25)+(i*200)+150+screen_height) - 1050
        screen[0][1] = (pygame.Surface((screen_width, (len(files)*300)+200), pygame.SRCALPHA))
        for i in range (len(files)):
            screen[0][1].blit(screen[1][i], (0, math.floor(i)))
        loading = False

        return(len(files))

def get_files(folder_path):
    """
    Returns a list containing the names of all files in the specified folder.
    """
    file_names = []
    try:
        for item in os.listdir(folder_path):
            if "".join(item[-5:]) == file_type:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    file_names.append(item)

    except os.error:
        os.mkdir(folder_path)
        
        for item in os.listdir(folder_path):
            if "".join(item[-5:]) == file_type:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    file_names.append(item)
    
    return file_names

def inrange(l, t, h, iseq=True):
    if iseq:
        out = l <= t <= h
    else:
        out = l < t < h
        
    return out

def open_file_explorer(select_folder=False, title="Select", filetypes=("All files", "*.*")):
    """
    Opens the OS file explorer and returns the selected path.

    Args:
        select_folder (bool): If True, opens a folder selector. If False, opens a file selector.
        title (str): Dialog title.
        filetypes (tuple): For file selection, a (label, pattern) tuple or list of such tuples.

    Returns:
        str|None: The selected path, or None if cancelled or on error.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    root = tk.Tk()

    root.withdraw()
    try:
        root.attributes("-topmost", True)
    except Exception:
        pass

    path = None
    try:
        if select_folder:
            path = filedialog.askdirectory(title=title)
        else:
            ft = filetypes
            if isinstance(filetypes, tuple) and isinstance(filetypes[0], str):
                ft = (filetypes,)
            path = filedialog.askopenfilename(title=title, filetypes=ft)
    except Exception:
        path = None
    finally:
        try:
            root.destroy()
        except Exception:
            pass

    if path == "" or path is None:
        return None
    return os.path.normpath(path)

def alph_list(data_list):
  """
  Alphabetizes a list of strings using the default character code
  (ASCII/Unicode) order, but performs a case-insensitive comparison
  by using str.lower as the sorting key.

  Args:
    data_list (list): The list of strings to sort.

  Returns:
    list: A new sorted list.
  """
  return sorted(data_list, key=str.lower)

def edit_str(instr, blinkpos):

    global charpressed

    if blinkpos > len(instr):
        blinkpos = len(instr)
            
    inlst = list(instr)
    
    if charpressed == "BACKSPACE":
        if blinkpos != 0:
            blinkpos -= 1
            try:
                del inlst[blinkpos]
            except Exception:
                pass

    elif charpressed == "UP":
        blinkpos = 0
        
    elif charpressed == "DOWN":
        blinkpos = len(inlst)
        
    elif charpressed == "LEFT":
        if blinkpos != 0:
            blinkpos -= 1
        
    elif charpressed == "RIGHT":
        if blinkpos != len(inlst):
            blinkpos += 1
    
    elif charpressed == "WORD_LEFT":
        if blinkpos > 0:
            i = blinkpos - 1
            while i > 0 and inlst[i].isspace():
                i -= 1
            while i > 0 and not inlst[i-1].isspace():
                i -= 1
            blinkpos = i
    
    elif charpressed == "WORD_RIGHT":
        L = len(inlst)
        i = blinkpos
        while i < L and inlst[i].isspace():
            i += 1
        while i < L and not inlst[i].isspace():
            i += 1
        blinkpos = i
        
    elif charpressed != "":
        s = charpressed
        for ch in s:
            dprint(f"appending {ch} to text")
            inlst.insert(blinkpos, ch)
            blinkpos += 1
    dprint("finishing type loop")
    
    return([list_to_string(inlst, ""), blinkpos])

def load(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    return(file_content)

def save(file_path, string):
    text_to_write = string
    norm_path = os.path.normpath(file_path)
    dirpath = os.path.dirname(norm_path)
    if dirpath:
        try:
            os.makedirs(dirpath, exist_ok=True)
        except Exception:
            pass

    with open(norm_path, "w", encoding="utf-8") as f:
        f.write(text_to_write)

def list_to_string(my_list, separator):
    if isinstance(my_list, str):
        return my_list
    return separator.join(map(str, my_list))

def string_to_list(my_string, separator):
    """Splits a string back into a list based on the separator."""
    return my_string.split(separator)

def merge_lists(list1, list2, pos):
    start = list1[:pos]
    
    smashed_item = list1[pos] + list2[0]

    end = list2[1:]
    
    return start + [smashed_item] + end

def get_text_width(text, font_size, font_name="Arial"):

    text = str(text)
    
    font_size += 1
    
    if not pygame.display.get_init():
        pygame.display.init()
    

    font = pygame.freetype.SysFont(font_name, font_size)
    
    text_rect = font.get_rect(text)
    
    return(text_rect.width)

def crop_lst(lst, croppos, rev=False):
    croppos = int(croppos)
    retlst = []
    if not rev:
        if croppos >= len(lst):
            return(lst)
        else:
            for i in range (croppos):
                retlst.append(lst[i])

    else:
        croppos = len(lst)-croppos
        lst.reverse()
        if croppos > len(lst):
            return(lst)
        else:
            for i in range (croppos):
                retlst.append(lst[i])
            retlst.reverse()
            
        

    return(retlst)

def button(text, font, x, y, butt_col, select_col, text_col, width, height, id, corner_round):
    """
    Draws a button on the screen and checks for mouse hover/click.
    """
    global button_pushed_states, mx, my, mc
    
    try:
        screen = pygame.display.get_surface() 
    except:
        dprint("Error: Pygame screen surface not found.")
        return
    
    button_rect = pygame.Rect(x, y, width, height)
    action = False
    current_col = butt_col

    if button_rect.collidepoint((mx, my)):
        current_col = select_col
        
        if mc[0] == 1:
            action = True
            
            if id not in button_pushed_states or button_pushed_states[id] == False:
                 button_pushed_states[id] = True 
    
    if id in button_pushed_states and button_pushed_states[id] == True and not action:
          button_pushed_states[id] = False

    sx, sy, sw, sh = button_rect
    if current_col == select_col:
        pygame.draw.rect(screen, select_col, (sx-2, sy-2, sw+4, sh+4), 0, corner_round)
    pygame.draw.rect(screen, butt_col, button_rect, 0, corner_round)



    try:
        rendered = font.render(text, fgcolor=text_col)
    except TypeError:
        rendered = font.render(text, True, text_col)

    if isinstance(rendered, tuple):
        text_surface, text_rect = rendered[0], rendered[1]
        try:
            text_rect.center = button_rect.center
        except Exception:
            text_rect = text_surface.get_rect(center=button_rect.center)
    else:
        text_surface = rendered
        text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

def get_butt_pushed(id):
    """
    Checks if a specific button was clicked in the last frame.
    """
    global button_pushed_states
    
    return button_pushed_states.get(id, False)

def tick_new():

    global typeselect, file_type, auto, auto_halt, mc, auto_launch, nxtc, file_count, recent_push, gtype, ntargcol, charpressed, new_menu, newname, name_edit, framen, disc_edit, newdisc, framene, framede, ani_x, ani_y, nbpos, dbpos

    menu_x, menu_y = 50, (screen_height//2)-new_animation
    menu_w, menu_h = (screen_width-50)-menu_x, ((screen_height//2)+new_animation)-menu_y

    name_def_w = menu_w-66
    
    ani_x, ani_y = font[25].get_rect("x").size
    
    exitRect = pygame.Rect(((menu_x+menu_w)-15, menu_y, 15, 18))
    
    pygame.draw.rect(screen[0][0], col[ntargcol], exitRect, 0, 0, 0, 3, 7, 0)
    font[25].render_to(screen[0][0], ((menu_x+menu_w)-15, menu_y), 'x', fgcolor=col[255])
    
    #Text detection for Description
    
    if exitRect.collidepoint((mx, my)):
        if ntargcol != 128:
            ntargcol += 8
    
        if mc[0]:
            new_menu = False
            name_edit = False
            disc_edit = False
    
    else:
        if ntargcol != 64:
            ntargcol -= 8
        
    if mc[0]:
        name_edit = False
        disc_edit = False
    
    if name_edit == disc_edit == False and charpressed == "ESCAPE":
        new_menu = False
    
    font[25].render_to(screen[0][0], (menu_x+2, menu_y+2), "New Game", fgcolor=col[255])
    
    if disc_edit:
        if charpressed == "ESCAPE":
            disc_edit = False
            
        if disc_edit:
            name_edit = False
            newdiscbpos = edit_str(newdisc, dbpos)
            charpressed = ""
            newdisc = newdiscbpos[0]
            dbpos = newdiscbpos[1]
            framede += 1

        else:
            framede = 0
    
    #Text processing for name

    if inrange(mx, menu_x+35, (menu_x+menu_w)-35) and inrange(my, menu_y+180, menu_y+280):
        pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+178, menu_w-66, 104), 0, 5)
        if mc[0]:
            disc_edit = True
    pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+180, menu_w-70, 100), 0, 5)

    if name_edit:
        if charpressed == "ESCAPE":
            name_edit = False
            
        if name_edit:
            disc_edit = False
            newnamebpos = edit_str(newname, nbpos)
            charpressed = ""
            newname = newnamebpos[0]
            nbpos = newnamebpos[1]
            framene += 1

        else:
            framene = 0

    if list(newname+"_")[0] == " ":
        newname = "".join(list(newname)[i+1] for i in range (len(list(newname))-1))
        nbpos -= 1
        
    # Imma be honest i have no clue whats happening here
    
    # Future self making an extra note, me neither. I just needed some code for a texbox to rename files bro, what is this?

    newname2 = newname if newname != "" else " "

    newname3 = newname2
    newname2 = newname2 if list(newname2)[-1] != " " else "".join([list(newname2)[i] for i in range (len(list(newname2))-1)])

    while newname2 != newname3:
        newname3 = newname2
        if newname2 != "":
            newname2 = newname2 if list(newname2)[-1] != " " else "".join([list(newname2)[i] for i in range (len(list(newname2))-1)])
        else:
            newname3 = newname2

    #post-processing

    precursname = list_to_string(crop_lst(list(newname2), nbpos, False), "")
    postcursname = list_to_string(crop_lst(list(newname2), nbpos, True), "")

    precursdisc = list_to_string(crop_lst(list(newdisc), dbpos, False), "")
    postcursdisc = list_to_string(crop_lst(list(newdisc), dbpos, True), "")
    
    #rendering
    
    if get_text_width(newname, 50) <= name_def_w:
        if inrange(mx, menu_x+35, menu_x+name_def_w+35) and inrange(my, menu_y+80, menu_y+130):
            pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+78, name_def_w+4, 54), 0, 5)
            if mc[0]:
                name_edit = True
        pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+80, name_def_w, 50), 0, 5)
    else:
        if inrange(mx, menu_x+35, menu_x+48+get_text_width(newname, 50)) and inrange(my, menu_y+80, menu_y+130):
            pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+78, get_text_width(newname, 50)+16, 54), 0, 5)
            if mc[0]:
                name_edit = True
        pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+80, get_text_width(newname, 50)+12, 50), 0, 5)


    if (framene/60)*2 % 1 <= 0.5 and name_edit:
        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+get_text_width(precursname, 50), menu_y+85, 2, 40))

    if (framede/60)*2 % 1 <= 0.5 and disc_edit:
        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+get_text_width(precursdisc, 15), menu_y+182, 1, 11))


    font[25].render_to(screen[0][0], (menu_x+35, menu_y+50), "Name", fgcolor=col[255])
    
    font[50].render_to(screen[0][0], (menu_x+37, menu_y+82), precursname+postcursname, fgcolor=col[255])

    font[25].render_to(screen[0][0], (menu_x+35, menu_y+148), "Description", fgcolor=col[255])

    desc_text = precursdisc + postcursdisc
    max_desc_width = menu_w - 70 - 4

    desc_lines = []
    for p in desc_text.split("\n"):
        if p == "":
            desc_lines.append("")
        else:
            desc_lines.extend(warp(font[15], p, max_desc_width))

    line_h = 16
    max_lines = 100 // line_h
    for idx, line in enumerate(desc_lines[:max_lines]):
        font[15].render_to(screen[0][0], (menu_x+37, menu_y+180 + idx * line_h), line, fgcolor=col[255])

    if (framede/60)*2 % 1 <= 0.5 and disc_edit:
        prec_text = precursdisc
        prec_lines = []
        for p in prec_text.split("\n"):
            if p == "":
                prec_lines.append("")
            else:
                prec_lines.extend(warp(font[15], p, max_desc_width))

        if prec_lines:
            caret_line = len(prec_lines) - 1
            caret_x = get_text_width(prec_lines[-1], 15)
        else:
            caret_line = 0
            caret_x = 0

        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+caret_x, menu_y+182 + caret_line * line_h, 1, 11))
    
    if not auto_halt:
        auto = "X" if auto_launch else ""

    button(auto, font[10], (menu_x+menu_w)-25, menu_y+25, col[48], col[128], col[255], 20, 20, 9999, 5)
    if get_butt_pushed(9999):
        if not auto_halt:
            auto_launch = not auto_launch
        auto_halt = True
    if not mc[0]:
        auto_halt = False
    
    font[18].render_to(screen[0][0], (((menu_x+menu_w)-25)-get_text_width("Immediatley load into editor: ", 18), menu_y+25), "Immediatley load into editor:", fgcolor=col[255])
        
    try:
        typeselect.draw(screen[0][0])
    except NameError:
        typeselect = pyselect.dropdown(types, font[25], menu_x+130, menu_y+10, 320, 60, col[48], col[128], col[255], col[16], col[32], 10, 10, False, False)

    if not mc[0]:
        recent_push = False

    if get_butt_pushed(0) and not recent_push:
        gtype = types[(types.index(gtype)+1) % (len(types))]
        recent_push = True

    button("CREATE!", font[40], ((menu_x+menu_w)-10)-get_text_width("CREATE!", 40), (menu_y+menu_h)-50, (32, 192, 32), col[128], col[255], get_text_width("CREATE!", 40)+5, 45, 1, 5)

    if get_butt_pushed(1):
        if newname == "":
            newname = "game"+str(file_count+1)
        dprint(f"Creating new game called {newname+file_type}")
        save(os.path.join(FILE_PATH, "Quickaccess", newname+file_type), list_to_string([newdisc, gtype], "\nbreak\n"))
        os.mkdir(os.path.join(FILE_PATH, "GAMES", newname))
        if auto_launch:
            global targ_item, run
            targ_item = newname
            run = False
        newname = ""
        newdisc = ""
        new_menu = False
        file_count = compile_files()


# Initialisations
if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()

    button_pushed_states = {}

    targ_item = ""

    nxtc = 0

    auto = ""

    auto_halt = False

    auto_launch = False

    recent_push = False

    gtype = "2D"

    types = ["2D"]

    nbpos = 0
    dbpos = 0

    col = [(i, i, i) for i in range (256)]

    font = [pygame.freetype.SysFont("Arial", size=i+1) for i in range (999)] # Create as many fonts as you could possibly need

    dprint(f"Debug: {debug}")

    screen_width = 1050
    screen_height = 750

    screen = []
    screen.append([None, None])

    screen[0][0] = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE) #why did i do this

    pygame.display.set_caption("Speaker Engine")

    icon = pygame.Surface((get_text_width("</>", 24), get_text_width("</>", 24)))

    icon.fill((col[243]))
    pygame.draw.rect(icon, col[0], (0, 0, icon.get_width(), icon.get_height()), 0, int(icon.get_width()/3.5))
    pygame.draw.rect(icon, col[48], (3, 3, icon.get_width()-6, icon.get_height()-6), 0, int(icon.get_width()/3.5))
    font[20].render_to(icon, ((get_text_width("</>", 24)//2)-(get_text_width("</>", 20)//2), (icon.get_height()//2)-10), "</>", fgcolor=(255, 127, 0))

    pygame.display.set_icon(icon)

    config = []

    try:
        config = string_to_list(load("Config"), "\nbreak\n")
        if config[0] == "":
            raise Exception("Config corrupted")
    except:
        config = ["az"]
        save("Config", list_to_string(config, "\nbreak\n"))

    sort_order = config[0]

    screenpos = 0
    screenpossmooth = 0.5
    screenspd = 0

    file_size_meas = ["Bytes", "KB", "MB", "GB", "TB"]

    sort_options = ["Alphabetical", "Reverse Alphabetical", "Recent", "Untouched", "Newest", "Oldest"]

    sort_order_lst = ["az", "za", "en", "eo", "bn", "bo"]

    sort_ord_opt = {
        sort_options[i]:sort_order_lst[i] for i in range (len(sort_options))
    }
    
    sort_ord_opt_invrt = {
            sort_order_lst[i]:sort_options[i] for i in range (len(sort_options))
        }

    max_dist = 0

    run = True

    framen = 0
    
    fs = False

    file_count = 0

    ntargcol = 64

    new_menu = False

    new_ani_fin = False

    clock = pygame.time.Clock()

    fps = 0

    new_animation = 0
    new_ani_spd = 0.5
    
    charpressed = ""

    newname = ""
    newdisc = ""
    name_edit = False
    disc_edit = False

    frameb = None
    framene = 0
    framede = 0

    del_menu = False


    dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 160))
    
    sort_halt = False

    loading = False

    nb = pyselect.button("+", font[75], screen_width-75, 0, 75, 75, col[64], col[128], col[255], 5)
    
    sodo = pyselect.dropdown(sort_options, font[25], screen_width-350, 10, 250, 55, col[64], col[128], col[255], col[16], col[48], 5, 5, False, False, sort_ord_opt_invrt[sort_order])

    framenl = []
    
    file_count = compile_files()
    top = pygame.Surface((screen_width, 86))
    for y in range (17):
        color = round(32 - y)
        pygame.draw.rect(top, (color, color, color), (0, 75 + y, screen_width, 1))

    # Main Loop
    while run:

        psw, psh = screen_width, screen_height
        screen_width, screen_height = screen[0][0].get_size()
        if (psw, psh) != (screen_width, screen_height):
            file_count = compile_files()
            top = pygame.Surface((screen_width, 86))
            for y in range (17):
                color = round(32 - y)
                pygame.draw.rect(top, (color, color, color), (0, 75 + y, screen_width, 1))
                
            dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            dark.fill((0, 0, 0, 160))

        nb.x, nb.y = screen_width-75, 0
        sodo.x, sodo.y = screen_width-350, 10

        screen[0][0].fill(col[24])

        charpressed = ""

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.TEXTINPUT:
                charpressed = e.text
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    charpressed = "ESCAPE"
                if e.key == pygame.K_BACKSPACE:
                    charpressed = "BACKSPACE"
                if e.key == pygame.K_LEFT:
                    charpressed = "LEFT"
                if e.key == pygame.K_RIGHT:
                    charpressed = "RIGHT"
                if e.key == pygame.K_F2:
                    debug = not debug
                if e.key == pygame.K_F11:
                    if fs:
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        fs = False
                    else:
                        pygame.display.set_mode((0, 0), pygame.RESIZABLE)
                        fs = True
                        
            if e.type == pygame.MOUSEWHEEL:
                screenspd -= e.y*15

        dprint(f"Keypressed: {charpressed if charpressed != "" else "None"}")

        mx, my = pygame.mouse.get_pos()
        mc = pygame.mouse.get_pressed()

        
        if skip:
            if charpressed == "BACKSPACE":
                skip = False
            else:
                if framen > 1:
                    skip = False
                    run = False
                    try:
                        targ_item = "".join(list(get_files(os.path.join(FILE_PATH, "Quickaccess"))[0])[0:-5])
                    except IndexError:
                        del targ_item
                        run = True

        if not (new_menu or del_menu) and charpressed == "ESCAPE":
            run = False

        screen[0][0].blit(top, (0, 0))

        screenspd *= screenpossmooth
        screenpos += screenspd

        if screenpos > max_dist:
            screenspd = 0
            screenpos = max_dist
        if screenpos < 0:
            screenspd = 0
            screenpos = 0

        if (file_count == 0 and framen > 15):
            font[40].render_to(screen[0][0], (screen_width//2 - 225, 75), "You dont have any Games yet!", fgcolor=col[255])
        elif loading:
            font[25].render_to(screen[0][0], (25, 90), "Loading...", fgcolor=col[255])


        screen[0][0].blit(screen[0][1], (0, 0 - screenpos))

        for i in range (file_count):
            if inrange(-40, math.floor((((i+3)*25)+(i*200)+135) - screenpos), screen_height):
                dprint(file_count)
                button("Delete", font[18], screen_width - 160, math.floor((((i+3)*25)+(i*200)+135) - screenpos), (192, 0, 0), (255, 32, 32), (255, 255, 255), 100, 40, i+2, 5)
                if get_butt_pushed(i+2) and int(((new_animation/(screen_height//4)))*50) == 0:
                    del_item = files[i]
                    dprint(list(del_item)[:-5])
                    del_item = "".join(list(del_item)[:-5])
                    del_menu = True
            if inrange(-40, math.floor((((i+3)*25)+(i*200)+85) - screenpos), screen_height):
                button("Open", font[18], screen_width - 160, math.floor((((i+3)*25)+(i*200)+85) - screenpos), (0, 192, 0), (32, 255, 32), (255, 255, 255), 100, 40, i+99999, 5)
                if get_butt_pushed(i+99999) and int(((new_animation/(screen_height//4)))*50) == 0:
                    del_item = files[i]
                    dprint(list(del_item)[:-5])
                    targ_item = "".join(list(del_item)[:-5])
                    run = False

        if del_menu:
            pygame.Surface.blit(screen[0][0], dark, (0, 0))
            pygame.draw.rect(screen[0][0], col[64], (100, 100, screen_width-200, screen_height-200), 0, 25)
            font[40].render_to(screen[0][0], (screen_width//2 - (get_text_width("Are you sure you want to delete "+del_item+"?", 40)//2), (screen_height//2)-100), "Are you sure you want to delete "+del_item+"?", fgcolor=col[255])
            button("No", font[30], (screen_width//2)-150, (screen_height//2), (0, 192, 0), (32, 255, 32), (255, 255, 255), 100, 50, 999999, 5)
            button("Yes", font[30], (screen_width//2)+50, (screen_height//2), (192, 0, 0), (255, 32, 32), (255, 255, 255), 100, 50, 999998, 5)
            if get_butt_pushed(999999):
                del_menu = False
            if get_butt_pushed(999998):
                del_menu = False
                os.remove(os.path.join(FILE_PATH, "Quickaccess", del_item+file_type))
                file_count = compile_files()
                loading = True
            if charpressed == "ESCAPE":
                del_menu = False

        pygame.draw.rect(screen[0][0], col[32], (0, 0, screen_width, 75))

        font[50].render_to(screen[0][0], (0, 12), f"SPEAKER ENGINE {("FPS: "+str(fps)) if debug else ""}", fgcolor=col[255])

        sodo.draw(screen[0][0])

        if not mc[0]:
            sort_halt = False
            
        nb.draw(screen[0][0])
        if nb.was_clicked():
            new_menu = True


        if new_menu:
            screen[0][0].blit(dark, (0, 0))
            if new_animation < screen_height//4:
                new_animation += new_ani_spd
                new_ani_spd *= 1.125
            if new_animation+(new_ani_spd*0) > screen_height//4:
                new_ani_fin = True
        else:
            new_ani_fin = False
            if new_ani_spd >= 0.5:
                new_ani_spd /= 1.125
                new_animation -= new_ani_spd

        if not new_ani_fin:
            if charpressed == "UP":
                screenspd -= 15
            if charpressed == "DOWN":
                screenspd += 15



        if new_animation >= 0.0625:

            for a in range (2):
                
                b = 10 if a == 0 else 3
                i = a*8

                na = not a
                ni = na*8

                center_col = int(((new_animation/(screen_height//4)))*50)
                if a == 0:
                    center_col = 50
                
                pygame.draw.rect(screen[0][0], col[center_col+(2*i)], (42+i, ((screen_height//2)-new_animation)-ni, (screen_width-100)+(ni*2), (new_animation*2)+(2*ni)), 0, b)
        if new_ani_fin:
            tick_new()
            

        loading = sort_ord_opt[sodo.get_selected()] != sort_order
        sort_order = sort_ord_opt[sodo.get_selected()]
        config[0] = sort_order

        if loading:
            dprint("Refreshing")
            loading = False
            file_count = compile_files()

        fps = int(clock.get_fps())
        fps = fps if fps != 0 else 1

        clock.tick(60)
        pygame.display.update()
        framen += 1

        framenl.append(fps)

        if framen % (60) == 0:
            dprint(config)
            dprint(list_to_string(config, "\nbreak\n"))

            save("Config", list_to_string(config, "\nbreak\n"))

            dprint(string_to_list(load("Config"), "\nbreak\n"))
            dprint("saved")
            if framen % 3600 == 0:
                file_count = compile_files()
                dprint("Reloaded Page")


    if targ_item != "":
        item = string_to_list(load(f"{FILE_PATH}Quickaccess{sep}{targ_item}{file_type}"), "\nbreak\n")
    else:
        pygame.quit()
        exit()

    dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 64))
    framen = 0

    screen[0][0].fill(col[0])
    font[25].render_to(screen[0][0], ((screen_width//2)-(get_text_width("Loading...", 25, "Arial")//2), (screen_height//2)-(25)), "Loading...", col[255])
    font[25].render_to(screen[0][0], ((screen_width//2)-(get_text_width("Do not close", 25, "Arial")//2), (screen_height//2)+(25)), "Do not close", col[255])
    pygame.display.update()
    game_name = targ_item

    q = multiprocessing.Queue()
    scan = multiprocessing.Process(target=recursive_scan, args=(os.path.join(FILE_PATH, "GAMES", game_name), q))
    scan.start()
    
    

    match item[1]:
        case "2D":
            run = True
            files = {}
            while run:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exit()
                if not scan.is_alive():
                    files = q.get()
                    scan.join()
                    dprint(files)
                    run = False

            run = True
            del screen
            pygame.quit()
            pygame.init()
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            pygame.display.set_icon(icon)
            pygame.display.set_caption(f"SPEAKER ENGINE - {game_name}")
            sw, sh = screen.get_size()
            
            font = [freetype.SysFont("Arial", s) for s in range (200)]

            width = 3

            fs = False
            framen = 0
            uhold = False
            bgrs = False
            exitbool = False

            update_rate = 1
            prevfiles = files
            ms = 0
            
            edit = editor(0.2, (sw-(2*(sw//5)), sh), font[20])

            kp = {pygame.K_BACKSPACE: 0, pygame.K_RETURN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

            while run:
                txtin = ""
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exitbool = True
                    if e.type == pygame.TEXTINPUT:
                        txtin = e.text
                    if e.type == pygame.KEYDOWN:
                        if e.key in kp:
                            kp[e.key] = 1
                    if e.type == pygame.KEYUP:
                        if e.key in kp:
                            kp[e.key] = 0
                            
                    if e.type == pygame.MOUSEWHEEL:
                        ms = e.y
                        
                for k, v in kp.items():
                    if v > 0:
                        kp[k] += 1
                    if v > 30 or v == 1:
                        if k == pygame.K_BACKSPACE: txtin = "BACKSPACE"
                        if k == pygame.K_RETURN: txtin = "RETURN"
                        if k == pygame.K_RIGHT: txtin = "RIGHT"
                        if k == pygame.K_LEFT: txtin = "LEFT"
                        if k == pygame.K_UP: txtin = "RIGHT"
                        if k == pygame.K_DOWN: txtin = "DOWN"
                    
                if (sw, sh) != screen.get_size():
                    sw, sh = screen.get_size()
                    edit.screen_size_x = sw-(2*(sw//5))
                    edit.screen_size_y = sh

                if framen % (60*update_rate) == (60*update_rate)/2 and not (bgrs or exitbool):
                    dprint("Updating files")
                    bgrs = True
                    q = multiprocessing.Queue()
                    scan = multiprocessing.Process(target=recursive_scan, args=(os.path.join(FILE_PATH, "GAMES", game_name), q, files))
                    scan.start()
                sw, sh = screen.get_size()
                screen.fill(col[16])

                mx, my = pygame.mouse.get_pos()
                mc = list(pygame.mouse.get_pressed())
                
                edit.code_update(txtin, ms)
                
                if uhold and mc[0]:
                    mc[0] = False
                elif mc[0]:
                    uhold = True
                else:
                    uhold = False
                
                dprint(mx, my)
                
                if prevfiles != files or (inrange(width, my, width+((sh//2)-4)) and inrange(width, mx, width+(sw//5-(width*2)))) or ld["menu_open"] or framen == 0:
                    filesurf, files = listfiles(game_name, files, txtin, (sw//5-(width*2), (sh//2)-4), (sw, sh), (width, width), mx, my, mc)
                    final_load = 2
                elif final_load == 2:
                    final_load = 1
                    
                if final_load == 1:
                    filesurf, files = listfiles(game_name, files, txtin, (sw//5-(width*2), (sh//2)-4), (sw, sh), (width, width), mx, my, mc)
                    final_load = 0
                    
                if bgrs and not q.empty():
                    final_load = 1
                
                pygame.draw.rect(screen, col[32], (0, 0, sw//5, sh))
                pygame.draw.rect(screen, col[128], (0, 0, sw//5, (sh//2)+(width//2)), width)
                pygame.draw.rect(screen, col[128], (0, (sh//2)-1, sw//5, (sh//2)+(width//2)), width)
                
                screen.blit(filesurf, (0, 0))
                
                edit.draw(screen, ((sw//5)-4, 0))

                if framen != 0:
                    pygame.display.update()
                clock.tick(60)
                fps = clock.get_fps()
                pygame.display.set_caption(f"SPEAKER ENGINE - {game_name} - {round(fps)}")


                if bgrs and not q.empty():
                    dprint("Filescan Finished")
                    bgrs = False
                    prevfiles = files
                    files = q.get()
                    scan.join()
                framen += 1
                if not (not (exitbool) or bgrs):
                    run = False
        case _:
            raise Exception("Bad game type")
        
pygame.quit()