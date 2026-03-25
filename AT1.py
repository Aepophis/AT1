

class Location:
    #Represents a location in the game world
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}  # Dictionary for N/S/E/W connections
    
    def display(self):
        #Print the location name and description#
        print(f"\n=== {self.name} ===")
        print(self.description)
    
    def set_connection(self, direction, location):
        #Set a connection to another location#

        
        self.connections[direction.upper()] = location


class Game:
    #Main game class that manages the adventure game#
    
    def __init__(self):
        # Initialize game state variables
        self.current_location = None
        self.health_score = 100  # Track overall health (0-100)
        self.energy_level = 100  # Track energy (0-100)
        self.stress_level = 0    # Track stress (0-100)
        self.tiredness = 0       # Track cumulative tiredness (0-100)
        self.sleep_hours = 8     # Start with proper sleep
        self.rest_deficit = 0    # Track cumulative rest deficit
        self.game_over = False
        self.current_day = 0     # Track which day of the week
        self.total_sleep_week = 8  # Track total sleep for the week
        self.day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.Location = {}
        self.create_locations()
        self.choices = {}  # Track choices made for each location
        # Time tracking (0-6 representing times of day)
        self.current_time = 0
        self.location_times_available = {}  # Track when locations are available
        # Track which actions have been used at each location today
        self.location_actions_used = {} 
        self.skipped_lunch = False
        self.ate_lunch = False
    
    def __str__(self, current_time):
        # Return a string representation of the current game time
        hours = current_time // 100
        minutes = current_time % 100
        if hours >= 12:
            hours -= 12 
        if hours == 0:
            hours = 12
        if hours >= 12:
            return f"Current time is{hours:2d}:{minutes:02d} PM"
        else:
            return f"Current time is{hours:2d}:{minutes:02d} AM"


    def create_locations(self):
        # Create location objects
        Bedroom = Location(
            "Your Bedroom",
            "You wake up after a night's sleep. Your room contains your bed, desk, and window.\n"
            "You need to decide how to start your day."
        )
        Kitchen = Location(
            "Kitchen",
            "The kitchen is where you can prepare meals. It has a fridge, stove, and dining table.\n"
            "You can choose to eat breakfast here or skip it."
        )
    
    def locational_choices(self):
        self.Location["bedroom"].location_choices = ["A", "B", "C"]
        self.Location["kitchen"].location_choices = ["A", "B", "C"]

    def create_location_choices(self):
        

        self.Location["bedroom"] = Bedroom
        self.Location["kitchen"] = Kitchen 



    def start_game(self):
        # Start the game by setting the initial location and displaying it
        self.current_location = self.Location["bedroom"]
        self.current_time = 600 # Start at 6:00 AM
        self.current_location.display()
        print(self.__str__(self.current_time))
        self.choices[self.current_location.name] = []  # Initialize choices for the bedroom




    def run(self):
        #Run the complete game
        self.start_game()


# Main program - Run the game
if __name__ == "__main__":
    game = Game()
    game.run()