from .button import Button

class Page:
    def __init__(self, buttons: list[Button], default_index: int = 0):
        self.buttons = buttons
        self.button_count = len(self.buttons)
        self.default_index = default_index
        self.index = default_index
    
    @property
    def page_height(self) -> int:
        return self.button_count * self.buttons[0].SURFACE_SIZE.y
    