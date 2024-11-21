# Concrete implementations for all screens.

from enum import StrEnum, auto
from screen_base import *
from db_connection import DBConnection
from screen_base import *
from screen_types import ScreenType

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

# Login screen.
class LoginScreen(Screen):
    def draw(self):
        printToScreen("Welcome to MyDKUHub! Please login!")

    def prompt(self):
        username = getUserInput("Username (leave empty to exit)")
        if not username:
            return ScreenType.EXIT, ()

        password = getUserInput("Password")
        if not password:
            return ScreenType.LOGIN, ()

        userLevel, userName = self.login(username[0], password[0])
        if userLevel is None:
            printToScreen("Unsuccessful login, please try again.")
            return ScreenType.LOGIN, ()

        self.session.user_level = userLevel
        self.session.user_name = userName  
        return ScreenType.HOME, ()

    def login(self, username, password):
        query = """
        SELECT li.type, 
               CASE 
                   WHEN li.type = 'student' THEN CONCAT(s.first_name, ' ', s.last_name)
                   WHEN li.type = 'instructor' THEN CONCAT(i.first_name, ' ', i.last_name)
                   ELSE 'Admin'
               END AS user_name
        FROM login_info li
        LEFT JOIN student s ON li.id = s.id
        LEFT JOIN instructor i ON li.id = i.id
        WHERE li.id = %s AND li.password = %s
        """
        result = self.db_connection.execute_query(query, (username, password))
        if result:
            return result[0]['type'], result[0]['user_name']
        return None, None


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
        printToScreen(f"Welcome {self.session.user_name}! Press ENTER to logout.")

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
