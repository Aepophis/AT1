class Location:
    # Represents a location in the game world
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}
        self.options = {}

    def display(self):
        print(f"\n=== {self.name} ===")
        print(self.description)

    def set_connection(self, direction, location):
        self.connections[direction.upper()] = location

    def add_option(self, text, period="all"):
        if period not in self.options:
            self.options[period] = []
        self.options[period].append(text)

    def get_options(self, period):
        result = []
        if "all" in self.options:
            result.extend(self.options["all"])
        if period in self.options:
            result.extend(self.options[period])
        return result

    def display_options(self, period):
        options = self.get_options(period)
        if not options:
            print("No options are available right now.")
            return
        for number, text in enumerate(options, 1):
            print(f"{number}. {text}")


class Game:
    # Main game class that manages the adventure game
    def __init__(self):
        self.current_location = None
        self.current_time = 600
        self.locations = {}
        self.create_locations()
        self.setup_options()

    def format_time(self):
        hours = self.current_time // 100
        minutes = self.current_time % 100
        time_frame = "AM"
        if hours >= 12:
            time_frame = "PM"
        if hours == 0:
            hours = 12 
        elif hours > 12:
            hours -= 12
        return f"{hours}:{minutes:02d} {time_frame}"

    def time_period(self):
        if 600 <= self.current_time < 1200:
            return "morning"
        if 1200 <= self.current_time < 1700:
            return "afternoon"
        if 1700 <= self.current_time < 2100:
            return "evening"
        return "night"

    def create_locations(self):
        bedroom = Location(
            "Bedroom",
            "Your room has a bed, a desk, and a window.\nYou can choose how to start the day."
        )
        kitchen = Location(
            "Kitchen",
            "The kitchen has a fridge and a stove.\nYou can prepare food or take a break here."
        )
        self.locations["bedroom"] = bedroom
        self.locations["kitchen"] = kitchen

    def setup_options(self):
        bedroom = self.locations["bedroom"]
        bedroom.add_option("Get up and start your day", "morning")
        bedroom.add_option("Scroll through your phone", "morning")
        bedroom.add_option("Lie down for a while", "afternoon")
        bedroom.add_option("Go back to sleep", "morning")
        bedroom.add_option("Go tosleep", "night")

        kitchen = self.locations["kitchen"]
        kitchen.add_option("Eat a healthy breakfast", "morning")
        kitchen.add_option("Skip breakfast", "morning")
        kitchen.add_option("Make tea", "afternoon")
        kitchen.add_option("Cook dinner", "evening")
        kitchen.add_option("Grab a snack", "night")
        kitchen.add_option("Grab a snack", "morning")
        kitchen.add_option("Grab a snack", "afternoon")

    def display_current_location(self):
        self.current_location.display()
        print("Time:", self.format_time())
        print("Options:")
        self.current_location.display_options(self.time_period())

    def start_game(self):
        self.current_location = self.locations["bedroom"]
        self.current_time = 600
        self.display_current_location()

    def run(self):
        self.start_game()


if __name__ == "__main__":
    game = Game()
    game.run()
