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
        self.show_end_menu()

    def scam_ending(self):
        print("\nYou fell for a scam. Always verify online information.")
        self.show_end_menu()

    def show_end_menu(self):
        while True:
            choice = input("\nWould you like to (1) Play Again or (2) Quit? Enter 1 or 2: ").strip()
            if choice == "1":
                self.__init__()  # Reset the game
                self.play()
            elif choice == "2":
                self.is_running = False
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

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
            "Check the suspicious message.", scam_site,
            outcome="You click on the link and are taken to a website that looks almost official..."))
        bedroom.add_option("ignore", Option(
            "Ignore the message and go to school.", school,
            outcome="You wisely decide to ignore the message and head to school."))

        school.add_option("listen", Option(
            "Listen to the cyber safety lesson.", computer_lab,
            outcome="Your teacher teaches you how to identify phishing scams and verify offers online."))
        school.add_option("ask", Option(
            "Ask your teacher about the message.", computer_lab,
            outcome="Your teacher warns you about the scam and shows you how to verify offers safely."))

        computer_lab.add_option("verify", Option(
            "Verify the message securely.", secure_site,
            outcome="You search for the official website and find that the offer is a scam!"))
        computer_lab.add_option("search", Option(
            "Search for information about the offer.", computer_lab,
            outcome="You search online and find several warning articles about this exact scam."))
        computer_lab.add_option("back", Option(
            "Go back to school.", school,
            outcome="You return to school to learn more from your teacher."))

        scam_site.add_option("enter", Option(
            "Enter personal details.", action=self.scam_ending,
            outcome="You enter your personal information and submit..."))
        scam_site.add_option("leave", Option(
            "Leave the suspicious website.", bedroom,
            outcome="Something doesn't feel right. You close the website and leave."))
        scam_site.add_option("warning", Option(
            "Read the warning signs on this site.", scam_site,
            outcome="You notice poor grammar, suspicious links, and urgent language - all red flags!"))

        secure_site.add_option("report", Option(
            "Report the scam.", action=self.safe_ending,
            outcome="You report the scam to the authorities and cybercriminals are caught!"))
        secure_site.add_option("read", Option(
            "Read more information about this offer.", secure_site,
            outcome="The official website shows the offer is legitimate and warns about the fake version."))
        secure_site.add_option("back", Option(
            "Go back to the computer lab.", computer_lab,
            outcome="You return to the computer lab to do more research."))

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
        print("Type north, south, east, west to move, or an action name.")

        while self.is_running:
            self.current_location.display()
            next_location = self.get_player_input()

            if isinstance(next_location, Location):
                self.current_location = next_location