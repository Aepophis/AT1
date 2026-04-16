# location.py
# Defines the Location class for game environments

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.options = {}
        self.directions = {}

    def add_option(self, key, option):
        self.options[key.lower()] = option

    def add_direction(self, direction, location):
        self.directions[direction.lower()] = location

    def display(self):
        print(f"\n=== {self.name} ===")
        print(self.description)

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