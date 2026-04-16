class Option:
    def __init__(self, text, action=None, key=None):
        self.text = text
        self.action = action
        self.key = key

    def run(self, game):
        if callable(self.action):
            self.action(game)
        elif isinstance(self.action, str):
            print(self.action)
        elif self.key in {"N", "E", "S", "W"}:
            game.move(self.key)
        else:
            print(f"You chose: {self.text}")
        print()


class Location:
    # Represents a location in the game world
    def __init__(self, name, description, x=0, y=0):
        self.name = name
        self.description = description
        self.coords = (x, y)
        self.connections = {}
        self.options = {}

    def display(self):
        print(f"\n=== {self.name} ===")
        print(f"Coordinates: {self.coords}")
        print(self.description)

    def set_connection(self, direction, location):
        self.connections[direction.upper()] = location

    def add_option(self, text, key, period="all", action=None):
        key = key.upper()
        if not (key in {"N", "E", "S", "W"} or key.isdigit()):
            raise ValueError("Option key must be N, E, S, W or a digit")
        if period not in self.options:
            self.options[period] = {}
        self.options[period][key] = Option(text, action, key)

    def get_options(self, period):
        result = {}
        if "all" in self.options:
            result.update(self.options["all"])
        if period in self.options:
            result.update(self.options[period])
        return result

    def display_options(self, period):
        options = self.get_options(period)
        if not options:
            print("No options are available right now.")
            return
        order = ["N", "E", "S", "W"]
        for direction in order:
            if direction in options:
                print(f"{direction}. {options[direction].text}")
        numeric_keys = sorted(k for k in options if k not in order)
        for key in numeric_keys:
            print(f"{key}. {options[key].text}")


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

    def get_direction_name(self, direction):
        return {
            "N": "north",
            "E": "east",
            "S": "south",
            "W": "west"
        }.get(direction.upper(), direction)

    def move(self, direction):
        direction = direction.upper()
        if direction not in self.current_location.connections:
            print("You can't move that way.")
            return
        destination = self.current_location.connections[direction]
        self.current_location = destination
        self.advance_time(10)
        print(f"You move {self.get_direction_name(direction)} to {destination.name}.")

    def create_locations(self):
        bedroom = Location(
            "Bedroom",
            "Your room has a bed, a desk, and a window.\nYou can choose how to start the day.",
            0,0
        )
        kitchen = Location(
            "Kitchen",
            "The kitchen has a fridge and a stove.\nYou can prepare food or take a break here.",
            0,1
        )
        outside_house = Location(
            "Outside House",
            "You can travel from place to place from here.\nWhere would you like to go?",
            1,0
        )
        self.locations["bedroom"] = bedroom
        self.locations["kitchen"] = kitchen
        self.locations["outside_house"] = outside_house

        bedroom.set_connection("N", kitchen)
        bedroom.set_connection("E", outside_house)
        kitchen.set_connection("S", bedroom)
        outside_house.set_connection("W", bedroom)

    def setup_options(self):
        bedroom = self.locations["bedroom"]
        bedroom.add_option("Go to the kitchen", "N", "morning")
        bedroom.add_option("Go outside", "E", "morning")
        bedroom.add_option("Scroll through your phone", "1", "morning", self.action_scroll_phone)
        bedroom.add_option("Lie down for a while", "2", "afternoon", self.action_lie_down)
        bedroom.add_option("Go back to sleep", "3", "morning", self.action_go_back_to_sleep)
        bedroom.add_option("Go to sleep", "4", "night", self.action_go_to_sleep)

        kitchen = self.locations["kitchen"]
        kitchen.add_option("Return to the bedroom", "S", "all")
        kitchen.add_option("Eat a healthy breakfast", "1", "morning", self.action_eat_breakfast)
        kitchen.add_option("Skip breakfast", "2", "morning", self.action_skip_breakfast)
        kitchen.add_option("Make tea", "3", "afternoon", self.action_make_tea)
        kitchen.add_option("Cook dinner", "4", "evening", self.action_cook_dinner)
        kitchen.add_option("Grab a snack", "5", "all", self.action_grab_snack)

        outside_house = self.locations["outside_house"]
        outside_house.add_option("Return home", "W", "all")
        outside_house.add_option("Walk to the park", "1", "morning", self.action_walk_park)
        outside_house.add_option("Go to the library", "2", "afternoon", self.action_go_library)
        outside_house.add_option("Visit a friend", "3", "evening", self.action_visit_friend)
        outside_house.add_option("Go to the gym", "4", "all", self.action_go_gym)
        outside_house.add_option("Go to school", "5", "morning", self.action_go_school)



    #Individual locational actions which will advance time and affect how the players feels, but not location    
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
        valid_names = {
            "NORTH": "N",
            "SOUTH": "S",
            "EAST": "E",
            "WEST": "W"
        }
        while True:
            choice = input("Choose an option (N/E/S/W, number, or Q to quit): ").strip().upper()
            if not choice:
                continue
            if choice == "Q":
                self.quit_requested = True
                return None
            choice = valid_names.get(choice, choice)
            options = self.get_available_options()
            if choice in options:
                return options[choice]
            print("Invalid choice. Please enter N, E, S, W, a number for an available option, or Q to quit.")

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

