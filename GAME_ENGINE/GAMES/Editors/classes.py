import pygame

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
    
    def get_inputs(fps=60, targfps=60, scrnps=int, scrnspd=int, hold_counters={}, hold_unicode={}) -> tuple:
        import pyperclip
        import time
        WORD_MOVE_INTERVAL = 30
        charpressed = ""
        running = True
    
        try:
            hold_counters.pop(pygame.K_ESCAPE, None)
            hold_unicode.pop(pygame.K_ESCAPE, None)
            hold_counters.pop(pygame.K_LSHIFT, None)
            hold_unicode.pop(pygame.K_LSHIFT, None)
            hold_counters.pop(pygame.K_RSHIFT, None)
            hold_unicode.pop(pygame.K_RSHIFT, None)
        except Exception:
            pass
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                scrnspd += event.y/-0.05
            if event.type == pygame.KEYDOWN:
                # Paste with Ctrl+V
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    try:
                        charpressed = pyperclip.paste()
                    except Exception:
                        charpressed = ""
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_ESCAPE:
                    charpressed = "ESCAPE"
                elif event.key == pygame.K_BACKSPACE:
                    charpressed = "BACKSPACE"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_UP:
                    charpressed = "UP"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_DOWN:
                    charpressed = "DOWN"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_LEFT and (event.mod & pygame.KMOD_CTRL):
                    charpressed = "WORD_LEFT"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_RIGHT and (event.mod & pygame.KMOD_CTRL):
                    charpressed = "WORD_RIGHT"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_LEFT:
                    charpressed = "LEFT"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_RIGHT:
                    charpressed = "RIGHT"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_RETURN:
                    charpressed = "ENTER"
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
                elif event.key == pygame.K_TAB:
                    charpressed = "TAB"
                else:
                    charpressed = event.unicode
                    hold_counters[event.key] = 0
                    hold_unicode[event.key] = event.unicode
            if event.type == pygame.KEYUP:
                try:
                    hold_counters.pop(event.key, None)
                    hold_unicode.pop(event.key, None)
                except Exception:
                    pass
                    
            keys = pygame.key.get_pressed()
    
        # Ensure we have an up-to-date key state each frame
        keys = pygame.key.get_pressed()
    
        repeat_delay = int(fps * (1/2)) if fps > 0 else int(targfps * (1/2))
        if repeat_delay < 1:
            repeat_delay = int(targfps * (1/2))
    
        if charpressed == "=" or charpressed == "+":
            new_menu = True
            
        try:
            mods_now = pygame.key.get_mods()
        except Exception:
            mods_now = 0
        try:
            if (mods_now & pygame.KMOD_CTRL):
                if keys[pygame.K_LEFT] or keys[pygame.K_COMMA]:
                    if time.time() - last_word_move_time >= WORD_MOVE_INTERVAL:
                        charpressed = "WORD_LEFT"
                        last_word_move_time = time.time()
                elif keys[pygame.K_RIGHT] or keys[pygame.K_PERIOD]:
                    if time.time() - last_word_move_time >= WORD_MOVE_INTERVAL:
                        charpressed = "WORD_RIGHT"
                        last_word_move_time = time.time()
        except Exception:
            pass
    
        for k in list(hold_counters.keys()):
            try:
                held = keys[k]
            except Exception:
                held = False
    
            if held:
                hold_counters[k] += 1
                if hold_counters[k] == 0 or hold_counters[k] >= repeat_delay:
                    if k == pygame.K_UP:
                        charpressed = "UP"
                    elif k == pygame.K_DOWN:
                        charpressed = "DOWN"
                    elif k == pygame.K_LEFT:
                        charpressed = "LEFT"
                    elif k == pygame.K_RIGHT:
                        charpressed = "RIGHT"
                    elif k == pygame.K_RETURN:
                        charpressed = "ENTER"
                    elif k == pygame.K_BACKSPACE:
                        charpressed = "BACKSPACE"
                    elif k == pygame.K_TAB:
                        charpressed = "TAB"
                    else:
                        try:
                            mods = pygame.key.get_mods()
                        except Exception:
                            mods = 0
                        if k == pygame.K_v and (mods & pygame.KMOD_CTRL):
                            try:
                                charpressed = pyperclip.paste()
                            except Exception:
                                charpressed = ""
                        elif (k == pygame.K_LEFT or k == pygame.K_COMMA) and (mods & pygame.KMOD_CTRL):
                            charpressed = "WORD_LEFT"
                        elif (k == pygame.K_RIGHT or k == pygame.K_PERIOD) and (mods & pygame.KMOD_CTRL):
                            charpressed = "WORD_RIGHT"
                        else:
                            charpressed = hold_unicode.get(k, pygame.key.name(k))
            else:
                hold_counters.pop(k, None)
                hold_unicode.pop(k, None)
        
        mx, my = pygame.mouse.get_pos()
        mc = pygame.mouse.get_pressed()

        scrnspd /= 2
        scrnps += scrnspd

        return charpressed, (mx, my, mc), running, scrnps, scrnspd, hold_counters, hold_unicode

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
        
