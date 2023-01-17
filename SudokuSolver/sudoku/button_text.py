import pygame

# Define colours
BG_COLOR = (204, 102, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
DEF_BUTTON = (200, 200, 200)


class States():
    def __init__(self):
        self.normal = 0
        self.hover = 1
        self.pressed = 2


BUTTON_STATES = States()


def invert_rgb(rgb_val):
    r_val = 255 - rgb_val[0]
    g_val = 255 - rgb_val[1]
    b_val = 255 - rgb_val[2]
    return (r_val, g_val, b_val)


def darken_rgb(rgb_val, ratio=2, steps=4):
    r_val = rgb_val[0] - int(ratio * (rgb_val[0] / steps))
    g_val = rgb_val[1] - int(ratio * (rgb_val[1] / steps))
    b_val = rgb_val[2] - int(ratio * (rgb_val[2] / steps))
    return (r_val, g_val, b_val)


def lighten_rgb(rgb_val, ratio=2, steps=4):
    r_val = rgb_val[0] + int(ratio * ((rgb_val[0] + 255) / steps))
    g_val = rgb_val[1] + int(ratio * ((rgb_val[1] + 255) / steps))
    b_val = rgb_val[2] + int(ratio * ((rgb_val[2] + 255) / steps))
    return (r_val, g_val, b_val)


class Button():
    def __init__(self, width, height, x, y, text, font, value,
                 btn_col=DEF_BUTTON, border_px=2, shading=True):
        # Rectangle
        self.rect = pygame.Rect(x, y, width, height)
        # State
        self.state = BUTTON_STATES.normal
        # Text
        self.text = text
        self.font = font
        # Value
        self.value = value
        # Colors
        self.button_col = btn_col
        self.darken_effect = False
        for i in self.button_col:
            if i > 128:
                self.darken_effect = True
                break
        if self.darken_effect:
            self.text_col = (0, 0, 0)
            self.border_color = (0, 0, 0)
            self.hover_col = darken_rgb(self.button_col)
            self.press_col = darken_rgb(self.button_col, 3)
        else:
            self.text_col = invert_rgb((0, 0, 0))
            self.border_color = invert_rgb((0, 0, 0))
            self.hover_col = lighten_rgb(self.button_col)
            self.press_col = lighten_rgb(self.button_col, 3)
        # Border (shading)
        self.border_thickness = border_px
        self.shading = shading

    def draw_button(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        # Set button state
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.state = BUTTON_STATES.pressed
            elif pygame.mouse.get_pressed()[0] == 0 and self.state == BUTTON_STATES.pressed:
                self.state = BUTTON_STATES.hover
                action = True
            else:
                self.state = BUTTON_STATES.hover
        else:
            self.state = BUTTON_STATES.normal
        # Draw button (state dependent)
        if self.state == BUTTON_STATES.normal:
            pygame.draw.rect(surface, self.button_col, self.rect)
        elif self.state == BUTTON_STATES.hover:
            pygame.draw.rect(surface, self.hover_col, self.rect)
        elif self.state == BUTTON_STATES.pressed:
            pygame.draw.rect(surface, self.press_col, self.rect)
        # Draw border (state and shading dependent)
        if self.shading:
            top_left = WHITE
            bottom_right = BLACK
        else:
            top_left = self.border_color
            bottom_right = self.border_color
        if self.state == BUTTON_STATES.hover or self.state == BUTTON_STATES.pressed:
            top_left = invert_rgb(top_left)
            bottom_right = invert_rgb(bottom_right)
        pygame.draw.line(surface, top_left, (self.rect.x, self.rect.y),
                         (self.rect.x + self.rect.width, self.rect.y), self.border_thickness)
        pygame.draw.line(surface, top_left, (self.rect.x, self.rect.y),
                         (self.rect.x, self.rect.y + self.rect.height), self.border_thickness)
        pygame.draw.line(surface, bottom_right, (self.rect.x, self.rect.y + self.rect.height),
                         (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self.border_thickness)
        pygame.draw.line(surface, bottom_right, (self.rect.x + self.rect.width, self.rect.y),
                         (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self.border_thickness)
        # Draw text (state dependent)
        col_val = self.text_col
        if self.state == BUTTON_STATES.hover or self.state == BUTTON_STATES.pressed:
            col_val = invert_rgb(self.text_col)
        text_img = self.font.render(self.text, True, col_val)
        text_rect = text_img.get_rect()
        text_rect.center = ((self.rect.x + (self.rect.width // 2),
                            self.rect.y + (self.rect.height // 2)))
        surface.blit(text_img, text_rect)
        # Return click action
        return action
