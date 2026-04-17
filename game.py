from location import Location
from option import Option


class Game:
    def __init__(self):
        self.is_running = True
        self.locations = {}
        self.current_location = None
        self.create_locations()

    def safe_ending(self):
        print("\nCongratulations! You avoided the scam.")
        self.is_running = False

    def scam_ending(self):
        print("\nYou fell for a scam. Always verify online information.")
        self.is_running = False

    def create_locations(self):
        bedroom = Location(
            "Your Bedroom",
            "You wake up and receive a suspicious message offering a prize."
        )

        street = Location(
            "Outside Your House",
            "You step outside and consider your next move."
        )

        school = Location(
            "School",
            "Your teacher is discussing cyber safety."
        )

        computer_lab = Location(
            "Computer Lab",
            "You access a computer to verify the message."
        )

        scam_site = Location(
            "Suspicious Website",
            "The website asks for personal details."
        )

        secure_site = Location(
            "Official Website",
            "You verify the offer on a legitimate website."
        )

        self.locations = {
            "bedroom": bedroom,
            "street": street,
            "school": school,
            "computer_lab": computer_lab,
            "scam_site": scam_site,
            "secure_site": secure_site,
        }

        # Directions
        bedroom.add_direction("north", street)

        street.add_direction("south", bedroom)
        street.add_direction("north", school)

        school.add_direction("south", street)
        school.add_direction("east", computer_lab)

        computer_lab.add_direction("west", school)

        # Options
        bedroom.add_option("check", Option(
            "Check the suspicious message.", scam_site))

        school.add_option("listen", Option(
            "Listen to the cyber safety lesson.", computer_lab))

        computer_lab.add_option("verify", Option(
            "Verify the message securely.", secure_site))

        scam_site.add_option("enter", Option(
            "Enter personal details.", action=self.scam_ending))

        scam_site.add_option("leave", Option(
            "Leave the suspicious website.", bedroom))

        secure_site.add_option("report", Option(
            "Report the scam.", action=self.safe_ending))

        self.current_location = bedroom

    def get_player_input(self):
        while True:
            command = input("\nEnter a direction or action: ").lower().strip()

            if command in ["quit", "exit"]:
                self.is_running = False
                return None

            next_location = self.current_location.get_next_location(command)
            if next_location:
                return next_location

            option = self.current_location.get_option(command)
            if option:
                result = option.execute()
                if result:
                    return result
                return self.current_location

            print("Invalid command. Try north, south, east, west, or an action.")

    def play(self):
        print("CYBER SAFETY: INTERACTIVE ADVENTURE")
        print("Type north, south, east, or west to move.")

        while self.is_running:
            self.current_location.display()
            next_location = self.get_player_input()

            if isinstance(next_location, Location):
                self.current_location = next_location