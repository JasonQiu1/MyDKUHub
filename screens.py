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
                "View Shopping Cart": (ScreenType.CLASS_RESULTS, ('shopping',)), 
                "View My Classes": (ScreenType.CLASS_RESULTS, ('enrolled',)),}
        
    def draw(self):
        printToScreen(f"Welcome {self.session.user_name}! Press ENTER to logout.")

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
        return ScreenType.HOME, ()
    
class ClassResultsScreen(Screen):
    def __init__(self, session, context):
        super().__init__(session)
        self.context = context  

    def draw(self):
        if self.context == 'enrolled':
            printToScreen(f"Enrolled Courses for {self.session.user_name}:")
            courses = self.get_enrolled_courses(self.session.user_netid)
        elif self.context == 'shopping':
            printToScreen(f"Shopping Cart for {self.session.user_name}:")
            courses = self.get_shopping_courses(self.session.user_netid)
        else:
            printToScreen("Unknown context.")
            return

        if not courses:
            printToScreen("No courses found.")
            return

        for course in courses:
            printToScreen(
                f"{course['year']} {course['term']} {course['session']} - "
                f"{course['course_id']} {course['course_name']} ({course['type']}) - "
                f"{course['dept_name']} - {course['credits']} credits - Grade: {course.get('grade', 'N/A')} - "
                f"Instructor: {course['instructor_first_name']} {course['instructor_last_name']}"
            )

    def prompt(self):
        printToScreen("Press ENTER to return to the Home Screen.")
        input()  
        return ScreenType.HOME, ()

    def get_enrolled_courses(self, student_id):
        query = """
        SELECT 
            c.id AS course_id,
            c.type AS type,
            c.name AS course_name,
            c.dept_name,
            c.credits,
            s.term,
            s.session,
            s.year,
            e.grade,
            i.first_name AS instructor_first_name,
            i.last_name AS instructor_last_name
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id AND s.type = c.type
        JOIN teaches t ON s.id = t.section_id
        JOIN instructor i ON t.instructor_id = i.id
        WHERE e.student_id = %s
        ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
        """
        return self.db_connection.execute_query(query, (student_id,))

    def get_shopping_courses(self, student_id):
        query = """
        SELECT 
            c.id AS course_id,
            c.type AS type,
            c.name AS course_name,
            c.dept_name,
            c.credits,
            s.term,
            s.session,
            s.year,
            i.first_name AS instructor_first_name,
            i.last_name AS instructor_last_name
        FROM shopping sh
        JOIN section s ON sh.section_id = s.id
        JOIN course c ON s.course_id = c.id AND s.type = c.type
        JOIN teaches t ON s.id = t.section_id
        JOIN instructor i ON t.instructor_id = i.id
        WHERE sh.student_id = %s
        ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
        """
        return self.db_connection.execute_query(query, (student_id,))
