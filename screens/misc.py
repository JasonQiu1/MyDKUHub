# Concrete implementations screens not organized into other files

from screens.base import *
from screens.ui import *
from screens.types import *

from db.utils import *
    
class ClassResultsScreen(Screen):
    def __init__(self, session, context):
        super().__init__(session)
        self.context = context

    def draw(self):
        if self.context == 'enrolled':
            printToScreen(f"Enrolled Courses for {self.session.user_name}:")
            courses = get_enrolled_courses(self.session.db_connection, self.session.user_netid)
        elif self.context == 'shopping':
            printToScreen(f"Shopping Cart for {self.session.user_name}:")
            courses = self.get_shopping_courses(self.session.user_netid)
        else:
            printToScreen("Unknown context.")
            return

        if not courses:
            printToScreen("No courses found.")
            return

        display_courses(courses)
    
    def prompt(self):
        if self.context == 'shopping':
            return self.handle_shopping_cart_actions()
        printToScreen("Press ENTER to return to the Home Screen.")
        input()  
        return ScreenType.HOME, ()


    def handle_shopping_cart_actions(self):
        courses = self.get_shopping_courses(self.session.user_netid)
        grouped_courses = group_courses_by_course_id(courses)

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
                result = self.session.db_connection.execute_procedure("enroll_selected_courses", (student_id, section_ids))
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
                    self.session.db_connection.execute_update("DELETE FROM shopping WHERE student_id = %s AND section_id = %s",
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
        JOIN instructor_master i ON t.instructor_id = i.id
        WHERE sh.student_id = %s
        ORDER BY s.year DESC, s.term, s.session, c.id, c.credits DESC;
        """
        return self.session.db_connection.execute_query(query, (student_id,))
    
class ClassSearchScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections_map = {}

    def draw(self):
        printToScreen("Class Search: Find Sections Matching Your Criteria")


    def prompt(self, swap = False):
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

        self.sections = get_course_sections(self.session.db_connection, year[0], term[0].lower(), session, dept_name, instructor_name)

        if self.sections:
            printToScreen("Matching Sections:")
            if self.session.user_level == 'student' or self.session.user_level == 'instructor':
                self.display_sections(self.sections)
                return self.prompt_action(swap)
            else:
                display_courses(self.sections, instructor=False)
                return self.prompt_action_admin()
        else:
            printToScreen("No matching sections found.")
            return ScreenType.HOME, ()



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
        departments = self.session.db_connection.execute_query(query)
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
        
    def prompt_action(self, swap = False):
        while True:  
            action = getUserInput("Enter the index of the section to see related sections, or press ENTER to return:")
            if not action or not action[0].isdigit():
                return ScreenType.HOME, ()  
            
            idx = int(action[0])
            if idx not in self.sections_map:
                printToScreen("Invalid index. Please try again.")
                continue  

            selected_section = self.sections_map[idx]
            related_sections = get_course_sections(
                self.session.db_connection, term=selected_section['term'], session=selected_section['session'], year=selected_section['year'],course_id = selected_section['course_id']
            )

            if not related_sections:
                printToScreen("No related sections found. Returning to main screen.")
                continue

            selected_section_ids = self.select_related_sections(related_sections)

            if not selected_section_ids:
                printToScreen("No sections selected. Returning to main screen.")
                continue

            combined_section_ids = ', '.join(map(str, selected_section_ids))  
            if swap:
                return ScreenType.CLASS_RESULTS, [combined_section_ids]

            if self.session.user_level == 'student':
                self.student_manage_sections_prompt(combined_section_ids)
            elif self.session.user_level == 'instructor':
                printToScreen()

    
    def student_manage_sections_prompt(self, combined_section_ids):
        next_action = getUserInput(f"Enter 'E' to enroll in sections {combined_section_ids}, 'A' to add to shopping cart")
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
    
    def prompt_action_admin(self):
        printToScreen("Admin manage sections prompt")
        return ScreenType.HOME, ()
        

    def select_related_sections(self, related_sections):
        selected_sections = {}
        sections_by_type = {}
        for section in related_sections:
            section_type = section['type']
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
            result = self.session.db_connection.execute_procedure("enroll_selected_courses", (student_id, section_ids))
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
                self.session.db_connection.execute_update(query, (student_id, section_id))
            return True
        except Exception as e:
            printToScreen(f"Error adding to shopping cart: {e}")
            return False




