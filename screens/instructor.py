# Screens specifically for instructors.

from screens.base import *
from screens.ui import *
from screens.types import *

from db.utils import *

class ViewTeachingClassesScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
        self.sections = []

    def draw(self):
        printToScreen(f"Teaching Classes for {self.session.user_name}")
        self.prompt_for_filters()

    def prompt(self):
        return self.prompt_for_course_selection()

    def prompt_for_filters(self):
        if self.session.user_level == 'admin':
            instructor_name = ' '.join(getUserInput("Enter instructor name (or press ENTER to skip)"))
            
        else:
            instructor_name = self.session.user_name
        year = getUserInput("Enter year (e.g., 2024): ")
        if not year or not year[0].isdigit():
            printToScreen("Invalid year. Returning to Home Screen.")
            return ScreenType.HOME, ()
        term = getUserInput("Enter term (e.g., spring, fall, summer): ")
        if not term or term[0].lower() not in ['spring', 'fall', 'summer']:
            printToScreen("Invalid term. Returning to Home Screen.")
            return ScreenType.HOME, ()
        self.sections = get_matching_sections(self.session.db_connection, year[0], term[0].lower(), None, None, instructor_name)

        if not self.sections:
            printToScreen("No classes found for the selected term and year.")
            return ScreenType.HOME, ()

        display_courses(self.sections, instructor=False)

    def prompt_for_course_selection(self):
        while True:
            course_input = getUserInput("Enter the index of a course to view or grade students, or press ENTER to return")
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

            printToScreen(f"Students Enrolled in {course_sections[0]['course_name']}")
            for idx, student in enumerate(merged_students):
                printToScreen(
                    f"{idx + 1}. {student['first_name']} {student['last_name']} - {student['student_id']} - Grade: {student.get('grade', 'N/A')}"
                )

            student_input = getUserInput("Enter the index of a student to change their grade, or press ENTER to return")
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
        new_grade = getUserInput(f"Enter the new grade for {student['first_name']} {student['last_name']} (or press ENTER to cancel)")
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
    
class AdviseesScreen(Screen):
    def draw(self):
        printToScreen("Your advisees")

class InstructorInformationScreen(Screen):
    def draw(self):
        printToScreen("Your personal information")
