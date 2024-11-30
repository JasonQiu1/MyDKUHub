# Base class for Screen.

from screens.types import *
from db_connection import DBConnection

# An abstract screen which can print stuff, get user input, and redirect to other screens.
class Screen:
    
    db_connection = None
    @classmethod
    def init_db(cls, host, user, password, database):
        cls.db_connection = DBConnection(host, user, password, database)
        cls.db_connection.connect()

    # IF YOU OVERRIDE THIS, MAKE SURE TO CALL super().__init__(session)
    def __init__(self, session):
        self.session = session

    # Draw the screen.
    # Do not handle user input here.
    # Returns nothing.
    def draw(self):
        print("Default screen, please implement.")

    # Prompt the user for input(s).
    # Perform any actions for that input.
    # Returns the next Screen that should occur based off that input
    #   AND with a tuple containing any arguments that should go into initializing that screen.
    def prompt(self):
        input("Default prompt, redirecting to LOGIN by default.")

        return ScreenType.LOGIN, ()
