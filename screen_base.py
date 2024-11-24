# Base classes and utilities functions for Screens.

from screen_types import *
from db_connection import DBConnection

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
        printToScreen("Default screen, please implement.")

    # Prompt the user for input(s).
    # Perform any actions for that input.
    # Returns the next Screen that should occur based off that input
    #   AND with a tuple containing any arguments that should go into initializing that screen.
    def prompt(self):
        getUserInput("Default prompt, redirecting to LOGIN by default.")

        return ScreenType.LOGIN, ()
    

    def get_enrolled_courses(self, student_id, term=None, session=None, year=None):
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
            s.id AS section_id,
            i.first_name AS instructor_first_name,
            i.last_name AS instructor_last_name
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id AND s.type = c.type
        JOIN teaches t ON s.id = t.section_id
        JOIN instructor i ON t.instructor_id = i.id
        WHERE e.student_id = %s
        """
        params = [student_id]

        # Add optional filters
        if term:
            query += " AND s.term = %s"
            params.append(term)
        if session:
            query += " AND s.session = %s"
            params.append(session)
        if year:
            query += " AND s.year = %s"
            params.append(year)

        query += " ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;"
        return self.db_connection.execute_query(query, tuple(params))


    def display_courses(self, courses):
        grouped_courses = self.group_courses_by_course_id(courses)

        for idx, (course_id, course_group) in enumerate(grouped_courses.items()):
            printToScreen(f"{idx + 1}. {course_group[0]['year']} {course_group[0]['term']} {course_group[0]['session']} - "
                          f"{course_group[0]['course_id']} {course_group[0]['course_name']} - {course_group[0]['dept_name']}")
            for subcourse in course_group:
                printToScreen(f"   - {subcourse['type']} (Section ID: {subcourse['course_id']}) - "
                              f"Instructor: {subcourse['instructor_first_name']} {subcourse['instructor_last_name']} - "
                              f"{subcourse['credits']} credits")