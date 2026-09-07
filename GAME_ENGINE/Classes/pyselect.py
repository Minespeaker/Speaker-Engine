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