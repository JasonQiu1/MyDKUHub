# Concrete implementations for all screens.

from enum import StrEnum, auto
from screen_base import *

# An exit screen. 
# Special screen in which prompt() is not called, so no implementation.
class ExitScreen(Screen):
    def draw(self):
        printToScreen("Thank you for using MyDKUHub!")

# All user levels available in the app.
class UserLevel(StrEnum):
    STUDENT = auto(),
    INSTRUCTOR = auto(),
    ADMINISTRATOR = auto(),

# A login screen.
class LoginScreen(Screen):
    def draw(self):
        printToScreen("Welcome to MyDKUHub! Please login!")

    def prompt(self):
        username = getUserInput("Username (leave empty to exit)")
        if not username:
            return ScreenType.EXIT, ()
        
        password = getUserInput("Password")
        if not password:
            password = [""]
        userLevel = self.login(username[0], password[0])
        if userLevel == None:
            print("Unsuccessful, please try again.")
            return False, ()

        self.session.userLevel = userLevel

        return ScreenType.HOME, ()

    # Login with the username and password.
    # Return the user's access level.
    # Return None if unsuccessful.
    def login(self, username, password):
        # TODO: IMPLEMENT
        return UserLevel.STUDENT


# User home screen. 
# Shows different options based on the session's userLevel.
class HomeScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        # TODO: create options based on the userLevel
        self.optionsToScreen = {
                "Search Classes": (ScreenType.LOGIN, ()), 
                "View Shopping Cart": (ScreenType.CLASS_RESULTS, ('TODO: INFO FOR QUERY FOR SHOPPING LIST')), 
                "View My Classes": (ScreenType.CLASS_RESULTS, ('TODO: INFO FOR QUERY FOR MY CLASSES'))}
    def draw(self):
        # TODO: display username instead of userlevel
        printToScreen(f"Welcome {self.session.userLevel.value.lower()}! Press ENTER to logout.")
    def prompt(self):
        userin = promptOptions(self.optionsToScreen.keys())
        if not userin:
            self.session.userLevel = None
            return ScreenType.LOGIN, ()
    
        if userin[0].isnumeric():
            optionIndex = int(userin[0])
            if optionIndex >= 0 and optionIndex < len(self.optionsToScreen):
                option = list(self.optionsToScreen.keys())[optionIndex]
                printToScreen(f"Selected '{option}'") # TODO: REMOVE AFTER DEBUGGING
                return self.optionsToScreen[option]

        printToScreen("Invalid option, please try again.")
        return False, ()
