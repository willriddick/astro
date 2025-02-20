from .button import Button

class Page:
    def __init__(self, buttons: list[Button], default_index: int = 0):
        self.buttons = buttons
        self.button_count = len(self.buttons)
        self.default_index = default_index
        self.button_index = default_index
    
    def change_index(self, input_dir: int):
        self.button_index = int((self.button_index + input_dir) % self.button_count)
    
    @property
    def selected_button(self) -> Button:
        return self.buttons[self.button_index]
    
    @property
    def page_height(self) -> int:
        return self.button_count * self.buttons[0].SURFACE_SIZE.y
    
    def render(self, display, position, draw_dir, alpha):
        for index, button in enumerate(self.buttons):
            button.update(hovered=index == self.button_index)
            surface = button.get_surface()
            y_offset = index * button.SURFACE_SIZE.y
            y_pos = position.y + y_offset

            if draw_dir == 1:  # top-to-bottom
                y_pos = position.y + y_offset
            else:  # bottom-to-top
                y_pos = position.y - self.page_height + y_offset
            
            surface.set_alpha(alpha)

            display.blit(surface, (position.x, y_pos))
