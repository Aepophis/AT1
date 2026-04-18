# Defines the Option class for player decisions

class Option:
    def __init__(self, description, next_location=None, action=None, outcome=None):
        self.description = description
        self.next_location = next_location
        self.action = action
        self.outcome = outcome

    def execute(self):
        # Display outcome message if it exists
        if self.outcome:
            print(f"\n> {self.outcome}")
        # Executes an optional action and returns the next location
        if self.action:
            self.action()
        return self.next_location