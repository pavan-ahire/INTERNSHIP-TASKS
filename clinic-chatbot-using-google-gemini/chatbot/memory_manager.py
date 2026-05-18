class MemoryManager:
    """
    Manages multi-turn conversation memory.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "parts": [message]
        })

    def add_bot_message(self, message: str):
        self.history.append({
            "role": "model",
            "parts": [message]
        })

    def get_history(self):
        return self.history

    def clear_memory(self):
        self.history = []