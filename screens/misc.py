# Concrete implementations screens not organized into other files

import plotext as plt

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
        JOIN instructor i ON t.instructor_id = i.id
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

        self.sections = get_matching_sections(self.session.db_connection, year[0], term[0].lower(), session, dept_name, instructor_name)

        if self.sections:
            printToScreen("Matching Sections:")
            if self.session.user_level == 'student' or self.session.user_level == 'instructor':
                self.display_sections(self.sections)
                return self.prompt_action()
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

            if self.session.user_level == 'student':
                self.student_manage_sections_prompt(combined_section_ids)
            elif self.session.user_level == 'instructor':
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
    
    def prompt_action_admin(self):
        printToScreen("Admin manage sections prompt")
        return ScreenType.HOME, ()
        

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
        return self.session.db_connection.execute_query(query, (course_id, term, session, year))

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

class ManageEnrollment(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections_map = {}

    def draw(self):
        printToScreen(f"Manage Enrollment for {self.session.user_name}:")
        enrolled_courses = get_enrolled_courses(self.session.db_connection, self.session.user_netid, term='fall', session='first', year='2024')

        if not enrolled_courses:
            printToScreen("You are not enrolled in any courses.")
            return
        display_courses(enrolled_courses)

    def prompt(self):
        action = promptOptions(["Drop Course", "Swap Course", "Return to Home"])
        
        if action[0] == "0":  # Drop Course
            return self.handle_drop_course()
        elif action[0] == "1":  # Swap Course
            return self.handle_swap_course()
        else:  # Return to Home
            return ScreenType.HOME, ()
    
    def handle_drop_course(self):
        courses = get_enrolled_courses(self.session.db_connection, self.session.user_netid, term='fall', session='first', year='2024')
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
        section_ids = ','.join(
            ','.join(str(course['section_id']) for course in group)
            for group in selected_course_groups
        )
        printToScreen({section_ids})
        self.drop_course(self.session.user_netid, section_ids)

        return ScreenType.MANAGE_ENROLLMENT, ()

    def handle_swap_course(self):
        courses = get_enrolled_courses(self.session.db_connection, self.session.user_netid, term='fall', session='first', year='2024')
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
            result = self.session.db_connection.execute_procedure("drop_course", (student_id, section_ids))
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
            result = self.session.db_connection.execute_procedure("swap_course", (student_id, drop_section_id,enroll_section_id))
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
        return ScreenType.HOME, ()

    def prompt_for_filters(self):
        year = getUserInput("Enter year (e.g., 2024): ")
        if not year or not year[0].isdigit():
            printToScreen("Invalid year. Returning to Home Screen.")
            return ScreenType.HOME, ()
        term = getUserInput("Enter term (e.g., spring, fall, summer): ")
        if not term or term[0].lower() not in ['spring', 'fall', 'summer']:
            printToScreen("Invalid term. Returning to Home Screen.")
            return ScreenType.HOME, ()
        self.sections = get_matching_sections(self.session.db_connection, year[0], term[0].lower(), None, None, self.session.user_name)

        if not self.sections:
            printToScreen("No classes found for the selected term and year.")
            return ScreenType.HOME, ()

        display_courses(self.sections, instructor=False)
        self.prompt_for_course_selection()

    def prompt_for_course_selection(self):
        while True:
            course_input = getUserInput("Enter the index of a course to view or grade students, or press ENTER to return:")
            if not course_input or not course_input[0].isdigit():
                return ScreenType.HOME, ()

            selected_index = int(course_input[0]) - 1
            grouped_courses = group_courses_by_course_id(self.sections)

            if selected_index < 0 or selected_index >= len(grouped_courses):
                printToScreen("Invalid selection. Please try again.")
                continue

            selected_course = list(grouped_courses.values())[selected_index]
            self.display_and_grade_students(selected_course)
            return ScreenType.HOME, ()


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
                self.session.db_connection.execute_update(query, (grade, student_id, section_id))
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
        return self.session.db_connection.execute_query(query, tuple(section_ids))
    
    

class PersonalInformationScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen(f"Personal Information for {self.session.user_name}:")
        personal_info = self.get_personal_information(self.session.user_netid)

        if not personal_info:
            printToScreen("No personal information found.")
            return
        
        printToScreen(
            f"Name: {personal_info['first_name']} {personal_info['last_name']}\n"
            f"Major: {personal_info.get('major', 'N/A')} (Immutable)\n"
            f"Class: {personal_info.get('class', 'N/A')} (Immutable)\n"
            f"Phone Numbers:\n{personal_info.get('phones', 'N/A')}\n"
            f"Addresses:\n{personal_info.get('addresses', 'N/A')}\n"
        )

    def prompt(self):
        action = promptOptions(["Update Phone", "Update Address", "Return to Home"])
        
        if action[0] == "0":  # Update Phone
            self.update_phone()
        elif action[0] == "1":  # Update Address
            self.update_address()
        else:  # Return to Home
            return ScreenType.HOME, ()
        
        return ScreenType.PERSONAL_INFORMATION, ()

    def get_personal_information(self, user_id):
        query_student = """
        SELECT first_name, last_name, major, class
        FROM student
        WHERE id = %s
        """
        student_info = self.session.db_connection.execute_query(query_student, (user_id,))
        if not student_info:
            return None

        query_phone = """
        SELECT type, country_code, area_code, number
        FROM phone_number
        WHERE student_id = %s
        """
        phone_numbers = self.session.db_connection.execute_query(query_phone, (user_id,))
        phones = "\n".join(
            f"{p['type'].capitalize()} Phone: +{p['country_code']} ({p['area_code']}) {p['number']}"
            for p in phone_numbers
        ) if phone_numbers else "N/A"

        query_address = """
        SELECT type, country, province, city, zip_code, street, street_number, unit
        FROM address
        WHERE student_id = %s
        """
        address_results = self.session.db_connection.execute_query(query_address, (user_id,))
        addresses = "\n".join(
            f"{a['type'].capitalize()} Address: {a['street_number']} {a['street']}, Unit {a.get('unit', 'N/A')}, "
            f"{a['city']}, {a['province']}, {a['country']}, ZIP: {a['zip_code']}"
            for a in address_results
        ) if address_results else "N/A"

        return {
            **student_info[0],
            "phones": phones,
            "addresses": addresses,
        }

    def update_phone(self):
        printToScreen("What would you like to do?")
        action = promptOptions(["Change an existing phone number", "Delete an existing phone number", "Insert a new phone number"])
        
        if action[0] == "0":  # Change an existing phone number
            self.change_phone_number()
        elif action[0] == "1":  # Delete an existing phone number
            self.delete_phone_number()
        elif action[0] == "2":  # Insert a new phone number
            self.insert_phone_number()
        else:
            printToScreen("Invalid action. Returning to Personal Information.")

    def change_phone_number(self):
        phone_type = getUserInput("Enter the phone type to update (work, cell, home):")
        if not phone_type or phone_type[0].lower() not in ['work', 'cell', 'home']:
            printToScreen("Invalid phone type. Returning to Personal Information.")
            return

        query = """
        SELECT id, country_code, area_code, number
        FROM phone_number
        WHERE student_id = %s AND type = %s
        """
        phone_numbers = self.session.db_connection.execute_query(query, (self.session.user_netid, phone_type[0].lower()))
        
        if not phone_numbers:
            printToScreen(f"No {phone_type[0]} phone numbers found. Returning to Personal Information.")
            return

        printToScreen(f"Existing {phone_type[0]} phone numbers:")
        for idx, phone in enumerate(phone_numbers):
            printToScreen(f"{idx + 1}: +{phone['country_code']} ({phone['area_code']}) {phone['number']}")

        selected_index = getUserInput("Enter the number of the phone to update:")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(phone_numbers):
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_phone_id = phone_numbers[selected_index]['id']

        country_code = getUserInput("Enter the new country code (e.g., 1 for US, 91 for India):")
        if not country_code or not country_code[0].isdigit():
            printToScreen("Invalid country code. Returning to Personal Information.")
            return

        area_code = getUserInput("Enter the new area code (e.g., 415 for San Francisco):")
        if not area_code or not area_code[0].isdigit():
            printToScreen("Invalid area code. Returning to Personal Information.")
            return

        number = getUserInput("Enter the new phone number (excluding area code):")
        if not number or not number[0].isdigit():
            printToScreen("Invalid phone number. Returning to Personal Information.")
            return

        update_query = """
        UPDATE phone_number
        SET country_code = %s, area_code = %s, number = %s
        WHERE id = %s
        """
        try:
            updated = self.session.db_connection.execute_update(
                update_query,
                (country_code[0], area_code[0], number[0], selected_phone_id)
            )
            if updated:
                printToScreen("Phone number updated successfully.")
            else:
                printToScreen("Failed to update phone number. Please try again.")
        except Exception as e:
            printToScreen(f"Error updating phone number: {e}")


    def delete_phone_number(self):
        phone_type = getUserInput("Enter the phone type to delete (work, cell, home):")
        if not phone_type or phone_type[0].lower() not in ['work', 'cell', 'home']:
            printToScreen("Invalid phone type. Returning to Personal Information.")
            return

        query = """
        SELECT id, country_code, area_code, number
        FROM phone_number
        WHERE student_id = %s AND type = %s
        """
        phone_numbers = self.session.db_connection.execute_query(query, (self.session.user_netid, phone_type[0].lower()))

        if not phone_numbers:
            printToScreen(f"No {phone_type[0]} phone numbers found. Returning to Personal Information.")
            return

        printToScreen(f"Existing {phone_type[0]} phone numbers:")
        for idx, phone in enumerate(phone_numbers):
            printToScreen(f"{idx + 1}: +{phone['country_code']} ({phone['area_code']}) {phone['number']}")

        selected_index = getUserInput("Enter the number of the phone to delete:")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(phone_numbers):
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_phone_id = phone_numbers[selected_index]['id']

        delete_query = """
        DELETE FROM phone_number
        WHERE id = %s
        """
        try:
            deleted = self.session.db_connection.execute_update(delete_query, (selected_phone_id,))
            if deleted:
                printToScreen("Phone number deleted successfully.")
            else:
                printToScreen("Failed to delete phone number. Please try again.")
        except Exception as e:
            printToScreen(f"Error deleting phone number: {e}")


    def insert_phone_number(self):
        phone_type = getUserInput("Enter phone type (work, cell, home):")
        if not phone_type or phone_type[0].lower() not in ['work', 'cell', 'home']:
            printToScreen("Invalid phone type. Returning to Personal Information.")
            return

        country_code = getUserInput("Enter the country code (e.g., 1 for US, 91 for India):")
        if not country_code or not country_code[0].isdigit():
            printToScreen("Invalid country code. Returning to Personal Information.")
            return

        area_code = getUserInput("Enter the area code (e.g., 415 for San Francisco):")
        if not area_code or not area_code[0].isdigit():
            printToScreen("Invalid area code. Returning to Personal Information.")
            return

        number = getUserInput("Enter the phone number (excluding area code):")
        if not number or not number[0].isdigit():
            printToScreen("Invalid phone number. Returning to Personal Information.")
            return

        query = """
        INSERT INTO phone_number (student_id, type, country_code, area_code, number)
        VALUES (%s, %s, %s, %s, %s)
        """

        try:
            self.session.db_connection.execute_update(
                query,
                (self.session.user_netid, phone_type[0].lower(), country_code[0], area_code[0], number[0])
            )
            printToScreen("Phone number inserted successfully.")
        except Exception as e:
            printToScreen(f"Failed to insert phone number: {e}")


    def update_address(self):
        printToScreen("What would you like to do?")
        action = promptOptions(["Add a new address", "Change an existing address", "Delete an address"])

        if action[0] == "0":  # Add a new address
            self.add_address()
        elif action[0] == "1":  # Change an existing address
            self.change_address()
        elif action[0] == "2":  # Delete an address
            self.delete_address()
        else:
            printToScreen("Invalid action. Returning to Personal Information.")

    def add_address(self):
        address_type = getUserInput("Enter address type (home, mail):")
        if not address_type or address_type[0].lower() not in ['home', 'mail']:
            printToScreen("Invalid address type. Returning to Personal Information.")
            return

        country = getUserInput("Enter country:")
        province = getUserInput("Enter province/state:")
        city = getUserInput("Enter city:")
        zip_code = getUserInput("Enter ZIP code (optional):")
        street = getUserInput("Enter street:")
        street_number = getUserInput("Enter street number:")
        unit = getUserInput("Enter unit number (optional):")

        query = """
        INSERT INTO address (student_id, type, country, province, city, zip_code, street, street_number, unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.session.db_connection.execute_update(
                query,
                (
                    self.session.user_netid, address_type[0].lower(),
                    country[0], province[0], city[0], zip_code[0] if zip_code else None,
                    street[0], street_number[0], unit[0] if unit else None
                )
            )
            printToScreen(f"{address_type[0].capitalize()} address added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add address: {e}")

    def change_address(self):
        query = """
        SELECT id, type, country, province, city, zip_code, street, street_number, unit
        FROM address
        WHERE student_id = %s
        """
        addresses = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        if not addresses:
            printToScreen("No addresses found. Returning to Personal Information.")
            return

        printToScreen("Existing addresses:")
        for idx, address in enumerate(addresses):
            printToScreen(
                f"{idx + 1}: {address['type'].capitalize()} Address: {address['street_number']} {address['street']}, "
                f"Unit {address.get('unit', 'N/A')}, {address['city']}, {address['province']}, {address['country']}, "
                f"ZIP: {address.get('zip_code', 'N/A')}"
            )

        selected_index = getUserInput("Enter the number of the address to update:")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(addresses):
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_address_id = addresses[selected_index]['id']

        country = getUserInput("Enter country:")
        province = getUserInput("Enter province/state:")
        city = getUserInput("Enter city:")
        zip_code = getUserInput("Enter ZIP code (optional):")
        street = getUserInput("Enter street:")
        street_number = getUserInput("Enter street number:")
        unit = getUserInput("Enter unit number (optional):")

        query = """
        UPDATE address
        SET country = %s, province = %s, city = %s, zip_code = %s, street = %s, street_number = %s, unit = %s
        WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(
                query,
                (
                    country[0], province[0], city[0], zip_code[0] if zip_code else None,
                    street[0], street_number[0], unit[0] if unit else None, selected_address_id
                )
            )
            printToScreen("Address updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update address: {e}")

    def delete_address(self):
        query = """
        SELECT id, type, country, province, city, zip_code, street, street_number, unit
        FROM address
        WHERE student_id = %s
        """
        addresses = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        if not addresses:
            printToScreen("No addresses found. Returning to Personal Information.")
            return

        printToScreen("Existing addresses:")
        for idx, address in enumerate(addresses):
            printToScreen(
                f"{idx + 1}: {address['type'].capitalize()} Address: {address['street_number']} {address['street']}, "
                f"Unit {address.get('unit', 'N/A')}, {address['city']}, {address['province']}, {address['country']}, "
                f"ZIP: {address.get('zip_code', 'N/A')}"
            )

        selected_index = getUserInput("Enter the number of the address to delete:")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(addresses):
            printToScreen("Invalid selection. Returning to Personal Information.")
            return

        selected_address_id = addresses[selected_index]['id']

        query = """
        DELETE FROM address
        WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(query, (selected_address_id,))
            printToScreen("Address deleted successfully.")
        except Exception as e:
            printToScreen(f"Failed to delete address: {e}")
            
            
class ShowMyProgressScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen(f"Academic Progress for {self.session.user_name}:\n")


    def prompt(self):
        options = [
            "Total Credits by Division",
            "Total Credits Earned",
            "Overall GPA",
            "GPA by Year and Term",
            "Return to Home Screen"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Total Credits by Division
            self.display_total_credits_by_division()
           
        elif user_choice[0] == "1":  # Total Credits Earned
            self.display_total_credits()
            
        elif user_choice[0] == "2":  # Overall GPA
            self.display_overall_gpa()
            
        elif user_choice[0] == "3":  # GPA by Year and Term
            self.display_gpa_by_year_term()
        elif user_choice[0] == "4":
            return ScreenType.HOME, ()  # Trigger navigation
        
        return ScreenType.MY_ACADEMIC_PROGRESS, ()
    
    def display_total_credits_by_division(self):
        total_credits_by_division = self.get_total_credits_by_division()
        printToScreen("Total Credits by Division:")
        for division, credits in total_credits_by_division.items():
            printToScreen(f"  {division}: {credits} credits")

    def display_total_credits(self):
        total_credits = self.get_total_credits()
        printToScreen(f"\nTotal Credits Earned: {total_credits} credits")

    def display_overall_gpa(self):
        gpa_overall = self.calculate_gpa()
        printToScreen(f"\nOverall GPA: {gpa_overall:.2f}")

    def display_gpa_by_year_term(self):
        gpa_by_year_term = self.calculate_gpa_by_year_term()
        printToScreen("\nGPA by Year and Term:")
        for year, terms in gpa_by_year_term.items():
            printToScreen(f"  Year {year}:")
            for term, gpa in terms.items():
                printToScreen(f"    {term}: {gpa:.2f}")

    def get_total_credits_by_division(self):
        query = """
        SELECT cd.division, SUM(c.credits) AS total_credits
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id
        JOIN course_division cd ON c.id = cd.course_id
        WHERE e.student_id = %s AND e.grade NOT IN ('F', 'NC')
        GROUP BY cd.division
        """
        results = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        return {row['division']: row['total_credits'] for row in results}

    def get_total_credits(self):
        query = """
        SELECT SUM(c.credits) AS total_credits
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id
        WHERE e.student_id = %s AND e.grade NOT IN ('F', 'NC')
        """
        result = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        return result[0]['total_credits'] if result else 0

    def calculate_gpa(self):
        grade_to_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0
        }
        query = """
        SELECT e.grade, c.credits
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id
        WHERE e.student_id = %s
        """
        results = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        total_points = sum(grade_to_points[row['grade']] * float(row['credits']) for row in results if row['grade'] in grade_to_points)
        total_credits = sum(float(row['credits']) for row in results if row['grade'] in grade_to_points)
        return total_points / total_credits if total_credits > 0 else 0.0

    def calculate_gpa_by_year_term(self):
        grade_to_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0
        }
        query = """
        SELECT s.year, s.term, e.grade, c.credits
        FROM enrollment e
        JOIN section s ON e.section_id = s.id
        JOIN course c ON s.course_id = c.id
        WHERE e.student_id = %s
        """
        results = self.session.db_connection.execute_query(query, (self.session.user_netid,))
        gpa_by_year_term = {}
        for row in results:
            year, term, grade, credits = row['year'], row['term'], row['grade'], float(row['credits'])
            if year not in gpa_by_year_term:
                gpa_by_year_term[year] = {}
            if term not in gpa_by_year_term[year]:
                gpa_by_year_term[year][term] = {'total_points': 0.0, 'total_credits': 0.0}
            if grade in grade_to_points:
                gpa_by_year_term[year][term]['total_points'] += grade_to_points[grade] * credits
                gpa_by_year_term[year][term]['total_credits'] += credits

        for year in gpa_by_year_term:
            for term in gpa_by_year_term[year]:
                data = gpa_by_year_term[year][term]
                gpa_by_year_term[year][term] = data['total_points'] / data['total_credits'] if data['total_credits'] > 0 else 0.0

        self.plot_gpa_chart(gpa_by_year_term)
        return gpa_by_year_term

    def plot_gpa_chart(self, gpa_by_year_term):

        plt.clear_figure()
        plt.title("GPA by Year and Term")
        plt.xlabel("Term and Year")
        plt.ylabel("GPA")

        x_labels = []  # Labels for the x-axis
        y_values = []  # Corresponding GPA values

        # Sort data by year, then by term priority (spring > fall > summer)
        for year in sorted(gpa_by_year_term.keys(), reverse=True):
            for term in ["spring", "fall", "summer"]:
                if term in gpa_by_year_term[year]:
                    x_labels.append(f"{term.capitalize()} {year}")  # Label format: term year
                    y_values.append(gpa_by_year_term[year][term])

        # Use bar chart for clear visualization
        plt.bar(x_labels, y_values, label="GPA")
        plt.ylim(0, 4.0)  # Set GPA range
        plt.show()



