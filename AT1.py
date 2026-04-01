class Option:
    def __init__(self, text, action=None):
        self.text = text
        self.action = action

    def run(self, game):
        if callable(self.action):
            self.action(game)
        elif isinstance(self.action, str):
            print(self.action)
        else:
            print(f"You chose: {self.text}")
        print()


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

    def add_option(self, text, period="all", action=None):
        if period not in self.options:
            self.options[period] = []
        self.options[period].append(Option(text, action))

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
        for number, option in enumerate(options, 1):
            print(f"{number}. {option.text}")


class Game:
    # Main game class that manages the adventure game
    def __init__(self):
        self.current_location = None
        self.current_time = 600
        self.locations = {}
        self.quit_requested = False
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

    def advance_time(self, minutes):
        hours = self.current_time // 100
        mins = self.current_time % 100
        total = hours * 60 + mins + minutes
        total %= 24 * 60
        new_hours = total // 60
        new_mins = total % 60
        self.current_time = new_hours * 100 + new_mins

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
        outside_house = Location(
            "Outside House",
            "You can travel from place to place from here.\nWhere would you like to go?"
        )
        self.locations["bedroom"] = bedroom
        self.locations["kitchen"] = kitchen
        self.locations["outside_house"] = outside_house

    def setup_options(self):
        bedroom = self.locations["bedroom"]
        bedroom.add_option("Get up and start your day", "morning", self.action_get_up)
        bedroom.add_option("Scroll through your phone", "morning", self.action_scroll_phone)
        bedroom.add_option("Lie down for a while", "afternoon", self.action_lie_down)
        bedroom.add_option("Go back to sleep", "morning", self.action_go_back_to_sleep)
        bedroom.add_option("Go to sleep", "night", self.action_go_to_sleep)

        kitchen = self.locations["kitchen"]
        kitchen.add_option("Eat a healthy breakfast", "morning", self.action_eat_breakfast)
        kitchen.add_option("Skip breakfast", "morning", self.action_skip_breakfast)
        kitchen.add_option("Make tea", "afternoon", self.action_make_tea)
        kitchen.add_option("Cook dinner", "evening", self.action_cook_dinner)
        kitchen.add_option("Grab a snack", "all", self.action_grab_snack)

        outside_house = self.locations["outside_house"]
        outside_house.add_option("Walk to the park", "morning", self.action_walk_park)
        outside_house.add_option("Go to the library", "afternoon", self.action_go_library)
        outside_house.add_option("Visit a friend", "evening", self.action_visit_friend)
        outside_house.add_option("Go to the gym", "all", self.action_go_gym)
        outside_house.add_option("Go to school", "morning", self.action_go_school)
        outside_house.add_option("Return home", "all", self.action_return_home)

    def action_get_up(self, game):
        print("You get out of bed and start moving. Time passes as you get ready.")
        self.advance_time(30)
        self.current_location = self.locations["kitchen"]

    def action_scroll_phone(self, game):
        print("You scroll through your phone and lose track of time.")
        self.advance_time(45)

    def action_lie_down(self, game):
        print("You lie down for a little while to relax.")
        self.advance_time(60)

    def action_go_back_to_sleep(self, game):
        print("You fall asleep again for a short nap.")
        self.advance_time(90)

    def action_go_to_sleep(self, game):
        print("You go to sleep completely and wake up later.")
        self.advance_time(480)

    def action_eat_breakfast(self, game):
        print("You eat a healthy breakfast and feel energized.")
        self.advance_time(30)
        self.current_location = self.locations["outside_house"]

    def action_skip_breakfast(self, game):
        print("You skip breakfast to save time, but you feel a little hungry.")
        self.advance_time(15)
        self.current_location = self.locations["outside_house"]

    def action_make_tea(self, game):
        print("You make a warm cup of tea. It helps you relax.")
        self.advance_time(20)

    def action_cook_dinner(self, game):
        print("You cook dinner and enjoy a nice meal.")
        self.advance_time(45)

    def action_grab_snack(self, game):
        print("You grab a snack quickly.")
        self.advance_time(10)

    def action_walk_park(self, game):
        print("You walk to the park and enjoy the fresh air.")
        self.advance_time(30)

    def action_go_library(self, game):
        print("You visit the library and spend some quiet time reading.")
        self.advance_time(40)

    def action_visit_friend(self, game):
        print("You visit a friend and have a good conversation.")
        self.advance_time(60)

    def action_go_gym(self, game):
        print("You go to the gym for a workout.")
        self.advance_time(50)

    def action_go_school(self, game):
        print("You head to school to attend classes.")
        self.advance_time(35)

    def action_return_home(self, game):
        print("You return home to rest.")
        self.advance_time(20)
        self.current_location = self.locations["bedroom"]

    def get_available_options(self):
        return self.current_location.get_options(self.time_period())

    def display_current_location(self):
        self.current_location.display()
        print("Time:", self.format_time())
        print("Options:")
        self.current_location.display_options(self.time_period())
        print("Q. Quit")

    def prompt_choice(self):
        while True:
            choice = input("Choose an option number (or Q to quit): ").strip()
            if not choice:
                continue
            if choice.lower() == "q":
                self.quit_requested = True
                return None
            if choice.isdigit():
                index = int(choice) - 1
                options = self.get_available_options()
                if 0 <= index < len(options):
                    return options[index]
            print("Invalid choice. Please enter the number of an available option or Q to quit.")

    def start_game(self):
        self.current_location = self.locations["bedroom"]
        self.current_time = 600
        self.quit_requested = False
        print("Welcome to the adventure game!")

    def run(self):
        self.start_game()
        while not self.quit_requested:
            self.display_current_location()
            option = self.prompt_choice()
            if option is None:
                break
            option.run(self)
        print("Thanks for playing!")


if __name__ == "__main__":
    game = Game()
    game.run()
