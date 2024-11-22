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
                "Search Classes": (ScreenType.CLASS_SEARCH, ()), 
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

        self.display_courses(courses)

    def prompt(self):
        if self.context == 'shopping':
            return self.handle_shopping_cart_actions()
        printToScreen("Press ENTER to return to the Home Screen.")
        input()  # Wait for user to press Enter
        return ScreenType.HOME, ()

    def display_courses(self, courses):
        grouped_courses = self.group_courses_by_course_id(courses)

        for idx, (course_id, course_group) in enumerate(grouped_courses.items()):
            printToScreen(f"{idx + 1}. {course_group[0]['year']} {course_group[0]['term']} {course_group[0]['session']} - "
                          f"{course_group[0]['course_id']} {course_group[0]['course_name']} - {course_group[0]['dept_name']}")
            for subcourse in course_group:
                printToScreen(f"   - {subcourse['type']} (Section ID: {subcourse['course_id']}) - "
                              f"Instructor: {subcourse['instructor_first_name']} {subcourse['instructor_last_name']} - "
                              f"{subcourse['credits']} credits")

    def handle_shopping_cart_actions(self):
        courses = self.get_shopping_courses(self.session.user_netid)
        grouped_courses = self.group_courses_by_course_id(courses)

        user_input = getUserInput("Enter the numbers of the courses to manage (comma-separated, or press ENTER to return):")
        if not user_input:
            return ScreenType.HOME, ()

        try:
            selected_indices = [int(idx.strip()) - 1 for idx in user_input[0].split(',') if idx.strip().isdigit()]
        except ValueError:
            printToScreen("Invalid input. Please try again.")
            return False, ()

        selected_course_groups = []
        for idx in selected_indices:
            if idx < 0 or idx >= len(grouped_courses):
                printToScreen(f"Invalid selection: {idx + 1}. Skipping.")
                continue
            selected_course_groups.append(list(grouped_courses.values())[idx])

        if not selected_course_groups:
            printToScreen("No valid courses selected.")
            return False, ()

        printToScreen(f"Selected courses: {[group[0]['course_name'] for group in selected_course_groups]}")

        action = promptOptions(["Enroll", "Delete"])
        if action[0] == "0":  # Enroll
            self.enroll_selected_courses(self.session.user_netid, selected_course_groups)
        elif action[0] == "1":  # Delete
            self.delete_selected_courses(self.session.user_netid, selected_course_groups)
        else:
            printToScreen("Invalid action. Returning to shopping cart.")
            return False, ()

        return ScreenType.CLASS_RESULTS, ('shopping',)

    def enroll_selected_courses(self, student_id, selected_course_groups):
        for course_group in selected_course_groups:
            section_ids = ','.join(str(course['section_id']) for course in course_group)
            try:
                result = self.db_connection.execute_procedure("enroll_selected_courses", (student_id, section_ids))
                if result is None:
                    return True  
                else:
                    printToScreen(f"Enrollment failed with message: {result}")
                    return False
            except Exception as e:
                printToScreen(f"Error during enrollment: {e}")
                return False

    def delete_selected_courses(self, student_id, selected_course_groups):
        for course_group in selected_course_groups:
            for course in course_group:
                try:
                    self.db_connection.execute_update("DELETE FROM shopping WHERE student_id = %s AND section_id = %s",
                                                      (student_id, course['section_id']))
                    printToScreen(f"Successfully deleted section {course['section_id']} from shopping cart.")
                except Exception as e:
                    printToScreen(f"Error deleting section {course['section_id']}: {e}")

    def group_courses_by_course_id(self, courses):
        grouped_courses = {}
        for course in courses:
            course_id = course['course_id']
            if course_id not in grouped_courses:
                grouped_courses[course_id] = []
            grouped_courses[course_id].append(course)
        return grouped_courses

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
            s.id AS section_id,
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

    

class ClassSearchScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections_map = {}

    def draw(self):
        printToScreen("Class Search: Find Sections Matching Your Criteria")


    def prompt(self):
        # Collect mandatory inputs
        year = getUserInput("Enter year (e.g., 2024)")
        if not year or not year[0].isdigit():
            printToScreen("Invalid year. Returning to Home Screen.")
            return ScreenType.HOME, ()

        term = getUserInput("Enter term (e.g., spring, fall, summer)")
        if not term or term[0].lower() not in ['spring', 'fall', 'summer']:
            printToScreen("Invalid term. Returning to Home Screen.")
            return ScreenType.HOME, ()

        session = getUserInput("Enter session (first, second, semester, mini, or press ENTER for all)")
        session = session[0].lower() if session else None

        dept_name = self.select_department()
        instructor_name = getUserInput("Enter instructor name (or press ENTER to skip)")
        instructor_name = instructor_name[0] if instructor_name else None

        sections = self.get_matching_sections(year[0], term[0].lower(), session, dept_name, instructor_name)

        if sections:
            printToScreen("Matching Sections:")
            self.display_sections(sections)
        else:
            printToScreen("No matching sections found.")
            return ScreenType.HOME, ()

        return self.prompt_action()

    def select_department(self):

        query = "SELECT name FROM dept"
        departments = self.db_connection.execute_query(query)
        if not departments:
            printToScreen("No departments found.")
            return None

        printToScreen("Select a department:")
        for idx, dept in enumerate(departments):
            printToScreen(f"{idx}: {dept['name']}")

        dept_index = getUserInput("Enter the index of the department (or press ENTER to skip)")
        if not dept_index or not dept_index[0].isdigit():
            return None

        dept_index = int(dept_index[0])
        if 0 <= dept_index < len(departments):
            return departments[dept_index]['name']
        else:
            printToScreen("Invalid index. Skipping department selection.")
            return None
    def get_matching_sections(self, year, term, session, dept_name, instructor_name):
        query = """
        SELECT 
            c.id AS course_id,
            c.name AS course_name,
            c.dept_name,
            c.credits,
            s.id AS section_id,
            s.type AS section_type,
            s.term,
            s.session,
            s.year,
            s.capacity,
            cl.building_name,
            cl.room_name,
            GROUP_CONCAT(
                DISTINCT CONCAT(i.first_name, ' ', i.last_name)
                ORDER BY i.first_name, i.last_name SEPARATOR '/'
            ) AS instructors,
            GROUP_CONCAT(
                DISTINCT CONCAT(st.day, ' ', DATE_FORMAT(ts.start_time, '%H:%i'), '-', DATE_FORMAT(ts.end_time, '%H:%i'))
                ORDER BY ts.start_time SEPARATOR ', '
            ) AS course_schedule
        FROM section s
        JOIN course c ON s.course_id = c.id AND s.type = c.type
        JOIN teaches t ON s.id = t.section_id
        JOIN instructor i ON t.instructor_id = i.id
        JOIN classroom cl ON s.building_name = cl.building_name AND s.room_name = cl.room_name
        JOIN section_time st ON s.id = st.section_id
        JOIN time_slot ts ON st.time_slot_id = ts.id
        WHERE s.year = %s AND s.term = %s
        """
        params = [year, term]

        if session:
            query += " AND s.session = %s"
            params.append(session)

        if dept_name:
            query += " AND c.dept_name = %s"
            params.append(dept_name)

        if instructor_name:
            query += """
            AND s.id IN (
                SELECT s_inner.id
                FROM section s_inner
                JOIN teaches t_inner ON s_inner.id = t_inner.section_id
                JOIN instructor i_inner ON t_inner.instructor_id = i_inner.id
                WHERE CONCAT(i_inner.first_name, ' ', i_inner.last_name) LIKE %s
            )
            """
            params.append(f"%{instructor_name}%")

        query += """
        GROUP BY 
            c.id, c.name, c.dept_name, c.credits, 
            s.id, s.type, s.term, s.session, s.year, s.capacity, 
            cl.building_name, cl.room_name
        ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
        """

        return self.db_connection.execute_query(query, tuple(params))

    def display_sections(self, sections):
        self.sections_map.clear()  # Reset sections map
        for idx, section in enumerate(sections):
            self.sections_map[idx] = section  # Store entire section details
            schedule = section['course_schedule'] or "No schedule available"
            printToScreen(
                f"{idx}: Course: {section['course_name']} ({section['course_id']}) - {section['dept_name']} - {section['credits']} credits\n"
                f"    Section ID: {section['section_id']} ({section['section_type']}) - Term: {section['term']} {section['session']} {section['year']}\n"
                f"    Instructors: {section['instructors']} - Location: {section['building_name']} {section['room_name']}\n"
                f"    Schedule: {schedule}\n"
            )


    def prompt_action(self):
        while True:  
            action = getUserInput("Enter the index of the section to see related sections, or press ENTER to return:")
            if not action or not action[0].isdigit():
                return ScreenType.HOME, ()  
            
            idx = int(action[0])
            if idx not in self.sections_map:
                printToScreen("Invalid index. Please try again.")
                continue  

            selected_section = self.sections_map[idx]

            related_sections = self.get_related_sections(
                selected_section['course_id'], selected_section['term'], selected_section['session'], selected_section['year']
            )

            if not related_sections:
                printToScreen("No related sections found. Returning to main screen.")
                continue

            selected_section_ids = self.select_related_sections(related_sections)

            if not selected_section_ids:
                printToScreen("No sections selected. Returning to main screen.")
                continue

            combined_section_ids = ', '.join(map(str, selected_section_ids))  

            next_action = getUserInput(f"Enter 'E' to enroll in sections {combined_section_ids} or 'A' to add to shopping cart:")
            if next_action and next_action[0].lower() == 'e':
                success = self.enroll_in_sections(self.session.user_netid, combined_section_ids)
                print('scucess', success)
                if success:
                    printToScreen(f"Successfully enrolled in sections {combined_section_ids}.")
                else:
                    printToScreen(f"Failed to enroll in sections {combined_section_ids}.")
            elif next_action and next_action[0].lower() == 'a':
                success = self.add_to_shopping_cart(self.session.user_netid, combined_section_ids)
                if success:
                    printToScreen(f"Successfully added sections {combined_section_ids} to your shopping cart.")
                else:
                    printToScreen(f"Failed to add sections {combined_section_ids} to your shopping cart.")
            else:
                printToScreen("Invalid action. Please try again.")

    
    def get_related_sections(self, course_id, term, session, year):
        query = """
        SELECT 
            s.id AS section_id,
            s.type AS section_type,
            c.id AS course_id,
            c.name AS course_name,
            c.dept_name,
            c.credits,
            s.term,
            s.session,
            s.year,
            cl.building_name,
            cl.room_name,
            GROUP_CONCAT(
                DISTINCT CONCAT(i.first_name, ' ', i.last_name)
                ORDER BY i.first_name, i.last_name SEPARATOR '/'
            ) AS instructors,
            GROUP_CONCAT(
                DISTINCT CONCAT(st.day, ' ', DATE_FORMAT(ts.start_time, '%H:%i'), '-', DATE_FORMAT(ts.end_time, '%H:%i'))
                ORDER BY ts.start_time SEPARATOR ', '
            ) AS course_schedule
        FROM section s
        JOIN course c ON s.course_id = c.id AND s.type = c.type
        JOIN teaches t ON s.id = t.section_id
        JOIN instructor i ON t.instructor_id = i.id
        JOIN classroom cl ON s.building_name = cl.building_name AND s.room_name = cl.room_name
        JOIN section_time st ON s.id = st.section_id
        JOIN time_slot ts ON st.time_slot_id = ts.id
        WHERE c.id = %s AND s.term = %s AND s.session = %s AND s.year = %s
        GROUP BY 
            s.id, s.type, c.id, c.name, c.dept_name, c.credits, 
            s.term, s.session, s.year, cl.building_name, cl.room_name
        ORDER BY s.type, s.id
        """
        return self.db_connection.execute_query(query, (course_id, term, session, year))

    def select_related_sections(self, related_sections):
        selected_sections = {}
        sections_by_type = {}
        for section in related_sections:
            section_type = section['section_type']
            if section_type not in sections_by_type:
                sections_by_type[section_type] = []
            sections_by_type[section_type].append(section)

        for section_type, sections in sections_by_type.items():
            printToScreen(f"Select a {section_type.upper()} section:")
            for idx, section in enumerate(sections):
                schedule = section['course_schedule'] or "No schedule available"
                printToScreen(
                    f"{idx}: Section ID: {section['section_id']} - Location: {section['building_name']} {section['room_name']}\n"
                    f"    Instructors: {section['instructors']}\n"
                    f"    Schedule: {schedule}\n"
                )

            while True:
                selected_idx = getUserInput(f"Enter the index of the {section_type.upper()} section:")
                if selected_idx and selected_idx[0].isdigit():
                    selected_idx = int(selected_idx[0])
                    if 0 <= selected_idx < len(sections):
                        selected_sections[section_type] = sections[selected_idx]['section_id']
                        break
                    else:
                        printToScreen("Invalid index. Please try again.")
                else:
                    printToScreen("You must select one section of this type.")

        return list(selected_sections.values())

    def enroll_in_sections(self, student_id, section_ids):
        try:
            result = self.db_connection.execute_procedure("enroll_selected_courses", (student_id, section_ids))
            if result is None:
                return True  
            else:
                printToScreen(f"Enrollment failed with message: {result}")
                return False
        except Exception as e:
            printToScreen(f"Error during enrollment: {e}")
            return False


    def add_to_shopping_cart(self, student_id, section_ids):
        query = "INSERT INTO shopping (student_id, section_id) VALUES (%s, %s)"
        try:
            for section_id in section_ids.split(', '):
                self.db_connection.execute_update(query, (student_id, section_id))
            return True
        except Exception as e:
            printToScreen(f"Error adding to shopping cart: {e}")
            return False

