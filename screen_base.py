# Base classes and utilities functions for Screens.

from screen_types import *

# Return the stripped user input split by spaces.
def getUserInput(prompt):
    return input(f"{prompt}: ").strip().split()

# Print the text to the screen.
def printToScreen(text):
    print(text)

# Prompt with numbered options, return the option that is selected.
# If not a number (or not in range), then return the user input.
def promptOptions(options):
    for idx, option in enumerate(options):
        printToScreen(f"{idx}: {option}")
    return getUserInput("Select an option by its number")

# An abstract screen which can print stuff, get user input, and redirect to other screens.
class Screen:
    # IF YOU OVERRIDE THIS, MAKE SURE TO CALL super().__init__(session)
    def __init__(self, session):
        self.session = session

    # Draw the screen.
    # Do not handle user input here.
    # Returns nothing.
    def draw(self):
        printToScreen("Default screen, please implement.")

    # Prompt the user for input(s).
    # Perform any actions for that input.
    # Returns the next Screen that should occur based off that input
    #   AND with a tuple containing any arguments that should go into initializing that screen.
    def prompt(self):
        getUserInput("Default prompt, redirecting to LOGIN by default.")

        return ScreenType.LOGIN, ()
