# location.py
# Defines the Location class for game environments

class Location:
    def __init__(self, name, description, alternative_descriptions=None):
        self.name = name
        self.description = description
        self.alternative_descriptions = alternative_descriptions or []
        self.visit_count = 0
        self.options = {}
        self.directions = {}

    def add_option(self, key, option):
        self.options[key.lower()] = option

    def add_direction(self, direction, location):
        self.directions[direction.lower()] = location

    def get_description(self):
        #Returns the appropriate description based on visit count.
        if self.visit_count == 0:
            return self.description
        # Cycle through alternative descriptions, then use a default return message
        alt_index = (self.visit_count - 1) % len(self.alternative_descriptions) if self.alternative_descriptions else -1
        if alt_index >= 0:
            return self.alternative_descriptions[alt_index]
        return f"You return to {self.name}."

    def visit(self):
        #Increment visit count and return the description for this visit.
        self.visit_count += 1
        return self.get_description()

    def display(self):
        print(f"\n=== {self.name} ===")
        print(self.get_description())

        if self.directions:
            print("\nAvailable Directions:")
            for direction in self.directions:
                print(f"- {direction.title()}")

        if self.options:
            print("\nAvailable Actions:")
            for key, option in self.options.items():
                print(f"- {key}: {option.description}")

    def get_next_location(self, command):
        return self.directions.get(command.lower())

    def get_option(self, command):
        return self.options.get(command.lower())