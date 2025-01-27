class Debug:
    _state = True
    _messages: list[str] = []

    @classmethod
    def update(cls) -> None:
        """Clears messages each frame."""
        cls._messages.clear()

    @classmethod
    def toggle(cls) -> None:
        """Toggles debug mode on/off."""
        cls._state = not cls._state

    @classmethod
    def enabled(cls) -> bool:
        """Returns whether debug mode is enabled."""
        return cls._state

    @classmethod
    def add_display(cls, text: str) -> None:
        """Adds a debug message to display."""
        cls._messages.append(text)

    @classmethod
    def display(cls) -> str:
        """Returns all debug messages as a formatted string."""
        return '\n'.join(cls._messages)
