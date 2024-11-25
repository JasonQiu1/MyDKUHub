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
        return ScreenType.HOME, (self.session.user_level,)

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
    def __init__(self, session, user_level):
        super().__init__(session)
        # TODO: create options based on the userLevel
        if user_level == 'student':
            self.optionsToScreen = {
                    "Search Classes": (ScreenType.CLASS_SEARCH, ()), 
                    "View Shopping Cart": (ScreenType.CLASS_RESULTS, ('shopping',)), 
                    "View My Classes": (ScreenType.CLASS_RESULTS, ('enrolled',)),
                    "Manage Enrollment": (ScreenType.MANAGE_ENROLLMENT, ()),
                }
        elif user_level == 'instructor':
            self.optionsToScreen = {
                    "Search Classes": (ScreenType.CLASS_SEARCH, ()), 
                    "View Teaching Classes": (ScreenType.TEACHING_CLASSES, ()),
                }
        elif user_level == 'admin':
            self.optionsToScreen = {
                    "Manage Classes": (ScreenType.CLASS_SEARCH, ()), 
                }
        
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
        return ScreenType.HOME, (self.session.user_level,)
    
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
        input()  
        return ScreenType.HOME, (self.session.user_level,)


    def handle_shopping_cart_actions(self):
        courses = self.get_shopping_courses(self.session.user_netid)
        grouped_courses = self.group_courses_by_course_id(courses)

        user_input = getUserInput("Enter the numbers of the courses to manage (comma-separated, or press ENTER to return):")
        if not user_input:
            return ScreenType.HOME, (self.session.user_level,)

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
            return ScreenType.HOME, (self.session.user_level,)

        term = getUserInput("Enter term (e.g., spring, fall, summer)")
        if not term or term[0].lower() not in ['spring', 'fall', 'summer']:
            printToScreen("Invalid term. Returning to Home Screen.")
            return ScreenType.HOME, (self.session.user_level,)

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
            return ScreenType.HOME, (self.session.user_level,)

        return self.prompt_action()

    def display_sections(self, sections):
        self.sections_map.clear()  # Reset sections map
        for idx, section in enumerate(sections):
            self.sections_map[idx] = section  # Store entire section details
            schedule = section['course_schedule'] or "No schedule available"
            printToScreen(
                f"{idx}: Course: {section['course_name']} ({section['course_id']}) - {section['dept_name']} - {section['credits']} credits\n"
                f"    Section ID: {section['section_id']} ({section['type']}) - Term: {section['term']} {section['session']} {section['year']}\n"
                f"    Instructors: {section['instructors']} - Location: {section['building_name']} {section['room_name']}\n"
                f"    Schedule: {schedule}\n"
            )

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
        
    def prompt_action(self):
        while True:  
            action = getUserInput("Enter the index of the section to see related sections, or press ENTER to return:")
            if not action or not action[0].isdigit():
                return ScreenType.HOME, (self.session.user_level,)  
            
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

            if self.session.user_level == 'student':
                self.student_manage_sections_prompt(combined_section_ids)
            elif self.session.user_level == 'instructor':
                printToScreen()
            elif self.session.user_level == 'admin':
                printToScreen()
    
    def student_manage_sections_prompt(self, combined_section_ids):
        next_action = getUserInput(f"Enter 'E' to enroll in sections {combined_section_ids}, 'A' to add to shopping cart:")
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
    
    def admin_manage_sections_prompt(self, combined_section_ids):
        printToScreen("Admin manage sections prompt")
        pass

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

class ManageEnrollment(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections_map = {}

    def draw(self):
        printToScreen(f"Manage Enrollment for {self.session.user_name}:")
        enrolled_courses = self.get_enrolled_courses(self.session.user_netid, term='fall', session='first', year='2024')

        if not enrolled_courses:
            printToScreen("You are not enrolled in any courses.")
            return
        self.display_courses(enrolled_courses)

    def prompt(self):
        action = promptOptions(["Drop Course", "Swap Course", "Return to Home"])
        
        if action[0] == "0":  # Drop Course
            return self.handle_drop_course()
        elif action[0] == "1":  # Swap Course
            return self.handle_swap_course()
        else:  # Return to Home
            return ScreenType.HOME, (self.session.user_level,)
    
    def handle_drop_course(self):
        courses = self.get_enrolled_courses(self.session.user_netid, term='fall', session='first', year='2024')
        grouped_courses = self.group_courses_by_course_id(courses)
        
        user_input = getUserInput("Enter the numbers of the courses to manage (comma-separated, or press ENTER to return):")
        if not user_input:
            return ScreenType.HOME, (self.session.user_level,)

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
        section_ids = ','.join(
            ','.join(str(course['section_id']) for course in group)
            for group in selected_course_groups
        )
        printToScreen({section_ids})
        self.drop_course(self.session.user_netid, section_ids)

        return ScreenType.MANAGE_ENROLLMENT, ()

    def handle_swap_course(self):
        courses = self.get_enrolled_courses(self.session.user_netid, term='fall', session='first', year='2024')
        grouped_courses = self.group_courses_by_course_id(courses)
        
        user_input = getUserInput("Enter the numbers of the courses to manage (comma-separated, or press ENTER to return):")
        if not user_input:
            return ScreenType.HOME, (self.session.user_level,)

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
        section_ids = ','.join(
            ','.join(str(course['section_id']) for course in group)
            for group in selected_course_groups
        )

        printToScreen("Searching for new sections to enroll in...")
        self.session.screen = ClassSearchScreen(self.session)
        new_screen_type, args = self.session.screen.prompt()

        if new_screen_type != ScreenType.CLASS_RESULTS or not args:
            printToScreen("No new sections selected. Returning to enrollment management.")
            return ScreenType.MANAGE_ENROLLMENT, ()

        new_section_ids =','.join(map(str, args))
        section_ids = section_ids 

        printToScreen(f"Selected new sections to enroll: {new_section_ids}")
        printToScreen(f"Selected new sections to drop: {section_ids}")

        self.swap_course(self.session.user_netid, section_ids, new_section_ids)

        return ScreenType.MANAGE_ENROLLMENT, ()

    def drop_course(self, student_id, section_ids):
        try:
            result = self.db_connection.execute_procedure("drop_course", (student_id, section_ids))
            if result is None:
                return True  
            else:
                printToScreen(f"Drop failed with message: {result}")
                return False
        except Exception as e:
            printToScreen(f"Error during drop: {e}")
            return False

    def swap_course(self, student_id, drop_section_id, enroll_section_id):
        printToScreen({drop_section_id,enroll_section_id})
        try:
            result = self.db_connection.execute_procedure("swap_course", (student_id, drop_section_id,enroll_section_id))
            if result is None:
                return True  
            else:
                printToScreen(f"Swap failed with message: {result}")
                return False
        except Exception as e:
            printToScreen(f"Error during swap: {e}")
            return False
        
class ViewTeachingClassesScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections = []

    def draw(self):
        printToScreen(f"Teaching Classes for {self.session.user_name}:")
        self.prompt_for_filters()

    def prompt(self):
        action = getUserInput("Press ENTER to return to the Home Screen.")
        return ScreenType.HOME, (self.session.user_level,)

    def prompt_for_filters(self):
        year = getUserInput("Enter year (e.g., 2024): ")
        if not year or not year[0].isdigit():
            printToScreen("Invalid year. Returning to Home Screen.")
            return ScreenType.HOME, (self.session.user_level,)
        term = getUserInput("Enter term (e.g., spring, fall, summer): ")
        if not term or term[0].lower() not in ['spring', 'fall', 'summer']:
            printToScreen("Invalid term. Returning to Home Screen.")
            return ScreenType.HOME, (self.session.user_level,)
        self.sections = self.get_matching_sections(year[0], term[0].lower(), None, None, self.session.user_name)

        if not self.sections:
            printToScreen("No classes found for the selected term and year.")
            return ScreenType.HOME, (self.session.user_level,)

        self.display_courses(self.sections, instructor=False)
        self.prompt_for_course_selection()

    def prompt_for_course_selection(self):
        while True:
            course_input = getUserInput("Enter the index of a course to view or grade students, or press ENTER to return:")
            if not course_input or not course_input[0].isdigit():
                return ScreenType.HOME, (self.session.user_level,)

            selected_index = int(course_input[0]) - 1
            grouped_courses = self.group_courses_by_course_id(self.sections)

            if selected_index < 0 or selected_index >= len(grouped_courses):
                printToScreen("Invalid selection. Please try again.")
                continue

            selected_course = list(grouped_courses.values())[selected_index]
            self.display_and_grade_students(selected_course)
            return ScreenType.HOME, (self.session.user_level,)


    def display_and_grade_students(self, course_sections):
        section_ids = [section['section_id'] for section in course_sections]
        while True:
            students = self.get_students_in_sections(section_ids)
            if not students:
                printToScreen("No students enrolled in this course.")
                return
            merged_students = self.merge_students_by_id(students)

            printToScreen(f"Students Enrolled in {course_sections[0]['course_name']}:")
            for idx, student in enumerate(merged_students):
                printToScreen(
                    f"{idx + 1}. {student['first_name']} {student['last_name']} - {student['student_id']} - Grade: {student.get('grade', 'N/A')}"
                )

            student_input = getUserInput("Enter the index of a student to change their grade, or press ENTER to return:")
            if not student_input or not student_input[0].isdigit():
                return

            selected_index = int(student_input[0]) - 1
            if selected_index < 0 or selected_index >= len(merged_students):
                printToScreen("Invalid selection. Please try again.")
                continue

            selected_student = merged_students[selected_index]
            self.prompt_for_grade_change(section_ids, selected_student)


    def merge_students_by_id(self, students):
        merged = {}
        for student in students:
            student_id = student['student_id']
            if student_id not in merged:
                merged[student_id] = {
                    "student_id": student['student_id'],
                    "first_name": student['first_name'],
                    "last_name": student['last_name'],
                    "grade": student.get('grade', 'N/A'),
                    "section_ids": []
                }
            merged[student_id]["section_ids"].append(student['section_id'])

        return list(merged.values())

    def prompt_for_grade_change(self, section_ids, student):
        new_grade = getUserInput(f"Enter the new grade for {student['first_name']} {student['last_name']} (or press ENTER to cancel):")
        if not new_grade:
            printToScreen("Grade change canceled.")
            return

        self.update_student_grades(section_ids, student['student_id'], new_grade[0])

    def update_student_grades(self, section_ids, student_id, grade):
        query = """
        UPDATE enrollment
        SET grade = %s
        WHERE student_id = %s AND section_id = %s
        """
        try:
            for section_id in section_ids:
                self.db_connection.execute_update(query, (grade, student_id, section_id))
            printToScreen(f"Successfully updated the grade for {student_id} to {grade} across all relevant sections.")
        except Exception as e:
            printToScreen(f"Failed to update grade: {e}")


    def get_students_in_sections(self, section_ids):
        query = f"""
        SELECT 
            s.id AS student_id,
            s.first_name,
            s.last_name,
            e.grade,
            e.section_id
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        WHERE e.section_id IN ({','.join(['%s'] * len(section_ids))})
        ORDER BY s.last_name, s.first_name;
        """
        return self.db_connection.execute_query(query, tuple(section_ids))
