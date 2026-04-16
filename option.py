# Defines the Option class for player decisions

class Option:
    def __init__(self, description, next_location=None, action=None):
        self.description = description
        self.next_location = next_location
        self.action = action

    def execute(self):
        # Executes an optional action and returns the next location
        if self.action:
            self.action()
        return self.next_location