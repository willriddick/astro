class Debug:
    """A global debug system for logging messages."""
    
    def __init__(self):
        self._state = False
        self._messages: list[str] = []

    @property
    def enabled(self) -> bool:
        """Returns whether debug mode is enabled."""
        return self._state

    @property
    def display(self) -> str:
        """Returns all debug messages as a formatted string."""
        return '\n'.join(self._messages)

    def update(self) -> None:
        """Clears messages each frame."""
        self._messages.clear()

    def toggle(self) -> None:
        """Toggles debug mode on/off."""
        self._state = not self._state

    def add_display(self, text: str) -> None:
        """Adds a debug message to display."""
        self._messages.append(text)


DEBUG = Debug()
