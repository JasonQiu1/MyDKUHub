from enum import StrEnum, auto

from screens.base import *
from screens.ui import *
from screens.types import ScreenType

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
        password = "1"
        if self.session.user_level != 'admin':
            password = getUserInput("Password")
            if not password:
                return ScreenType.LOGIN, ()   
        userLevel, userName = self.login(username[0], password[0])
        if userLevel is None:
            printToScreen("Unsuccessful login, please try again.")
            return ScreenType.LOGIN, ()
        self.session.user_level = userLevel
        self.session.user_name = userName  
        self.session.user_netid = username[0]
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
        WHERE li.id = %s 
        """
        print(password)
        if self.session.user_level != 'admin':
            query += "AND li.password = %s"
            result = self.session.db_connection.execute_query(query, (username, password))
        else:
            result = self.session.db_connection.execute_query(query, (username,))
        if result:
            return result[0]['type'], result[0]['user_name']
        return None, None

# User home screen. 
# Shows different options based on the session's userLevel.
class HomeScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        user_level = session.user_level
        if user_level == 'student':
            self.optionsToScreen = {
                    "Search Classes": (ScreenType.CLASS_SEARCH, ()), 
                    "View Shopping Cart": (ScreenType.CLASS_RESULTS, ('shopping',)), 
                    "View My Classes": (ScreenType.CLASS_RESULTS, ('enrolled',)),
                    "Manage Enrollment": (ScreenType.MANAGE_ENROLLMENT, ()),
                    "Personal Information": (ScreenType.PERSONAL_INFORMATION, ()),
                    "My Academic Prograss": (ScreenType.MY_ACADEMIC_PROGRESS,()),
                }
        elif user_level == 'instructor':
            self.optionsToScreen = {
                    "Search Classes": (ScreenType.CLASS_SEARCH, ()), 
                    "View Teaching Classes": (ScreenType.TEACHING_CLASSES, ()),
                    "View Advisees": (ScreenType.ADVISEES, ()),
                    "View Personal Information": (ScreenType.INSTRUCTOR_INFORMATION, ()),
                }
        elif user_level == 'admin':
            # TODO: finish options
            self.optionsToScreen = {
                    "Manage": (ScreenType.ADMIN, ()),
                    "Statistics": (ScreenType.STATISTICS, ()),  
                    "Sudo": (ScreenType.LOGIN, ()),
                    
                }
        
    def draw(self):
        printToScreen(f"Welcome {self.session.user_name}! Press ENTER to logout.")
        if self.user_level == 'student':
            printToScreen(f"Fetching hold information for {self.session.user_name}...")
            self.get_hold_info(self.session, self.session.user_netid)  # Use the student's ID

    def get_hold_info(self, session, student_id):
        query = """
        SELECT h.type AS hold_type
        FROM hold h
        WHERE h.student_id = %s;
        """
        results = session.db_connection.execute_query(query, (student_id,))
        if results:
            printToScreen("Hold(s) on your account:")
            for hold in results:
                printToScreen(f"- {hold['hold_type'].capitalize()} hold")
        else:
            printToScreen("No holds found on your account.")

    def prompt(self):
        userin = promptOptions(self.optionsToScreen.keys())
        if not userin:
            self.session.user_level = None
            self.session.user_name = None
            return ScreenType.LOGIN, ()

        if userin[0].isnumeric():
            optionIndex = int(userin[0])
            if 0 <= optionIndex < len(self.optionsToScreen):
                option = list(self.optionsToScreen.keys())[optionIndex]
                return self.optionsToScreen[option][0], (self.optionsToScreen[option][1])

        printToScreen("Invalid option, please try again.")
        return ScreenType.HOME, (self.session.user_level,)
