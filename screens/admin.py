from screens.base import *
from screens.ui import *
from screens.types import *
from screens.misc import *

class AdminScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen(f"Admin Panel for {self.session.user_name}:\n")

    def prompt(self):
        options = [
            "Manage Instructors",
            "Manage Departments",
            "Manage Students",
            "Manage Courses",
            "Manage Grades",
            "Return to Home Screen"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0": 
            return ScreenType.MANAGE_INSTRUCTOR, ()
        elif user_choice[0] == "1":
            return ScreenType.MANAGE_DEPARTMENT, ()
        elif user_choice[0] == "2": 
            return ScreenType.MANAGE_STUDENT, ()
        elif user_choice[0] == "3": 
            return ScreenType.MANAGE_COURSE, ()
        elif user_choice[0] == "4": 
            return ScreenType.TEACHING_CLASSES, ()
        elif user_choice[0] == "5":
            return ScreenType.HOME, ()
        return ScreenType.ADMIN, ()

class ManageInstructorScreen(Screen):
    def __init__(self, session):
        super().__init__(session)
    
    def getUserInput(prompt_message):
        input_value = input(f"{prompt_message}: ").strip()
        return [input_value] if input_value else []


    def draw(self):
        printToScreen("Manage Instructors:\n")
        
    def prompt(self):
        options = [
            "Search and Modify Instructor",
            "Insert New Instructor",
            "Delete Instructor",
            "Return to Admin Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  
            self.search_and_modify_instructor()
        elif user_choice[0] == "1":  
            self.insert_instructor()
        elif user_choice[0] == "2": 
            self.delete_instructor()
        elif user_choice[0] == "3": 
            return ScreenType.ADMIN, ()

        return ScreenType.MANAGE_INSTRUCTOR, ()

    def search_and_modify_instructor(self):
        first_name = getUserInput("Enter the instructor's first name (or leave empty for all):")
        last_name = getUserInput("Enter the instructor's last name (or leave empty for all):")

        first_name_filter = f"%{first_name[0]}%" if first_name else "%"
        last_name_filter = f"%{last_name[0]}%" if last_name else "%"

        query = """
        SELECT id, first_name, last_name, dept, salary, isDuke
        FROM instructor
        WHERE first_name LIKE %s AND last_name LIKE %s
        """
        results = self.session.db_connection.execute_query(query, (first_name_filter, last_name_filter))

        if not results:
            printToScreen("No instructors found matching the criteria.")
            return

        printToScreen("Instructors found:")
        for idx, instructor in enumerate(results):
            printToScreen(f"{idx + 1}. ID: {instructor['id']}, Name: {instructor['first_name']} {instructor['last_name']}, "
                        f"Department: {instructor['dept']}, Salary: {instructor['salary']}, Duke Status: {instructor['isDuke']}")

        selected_index = getUserInput("Enter the number of the instructor to modify (or press ENTER to return):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(results):
            printToScreen("Invalid selection.")
            return

        selected_instructor = results[selected_index]
        self.modify_instructor(selected_instructor['id'])


    def modify_instructor(self, instructor_id):
        new_first_name = getUserInput("Enter new first name (or press ENTER to skip):")
        new_last_name = getUserInput("Enter new last name (or press ENTER to skip):")

        dept_query = "SELECT name FROM dept"
        departments = self.session.db_connection.execute_query(dept_query)
        if not departments:
            printToScreen("No departments found. Please add departments first.")
            return

        printToScreen("Available Departments:")
        for idx, dept in enumerate(departments):
            printToScreen(f"{idx + 1}: {dept['name']}")

        new_dept_input = getUserInput("Enter new department name or select an index (or press ENTER to skip):")
        if new_dept_input and new_dept_input[0].isdigit():
            dept_index = int(new_dept_input[0]) - 1
            if 0 <= dept_index < len(departments):
                new_dept = departments[dept_index]['name']
            else:
                printToScreen("Invalid department selection. Skipping department change.")
                new_dept = None
        else:
            new_dept = new_dept_input[0] if new_dept_input else None

        new_salary = getUserInput("Enter new salary (or press ENTER to skip):")
        is_duke = getUserInput("Is this instructor a Duke employee? (yes/no, or press ENTER to skip):")

        update_query = """
        UPDATE instructor
        SET first_name = COALESCE(NULLIF(%s, ''), first_name),
            last_name = COALESCE(NULLIF(%s, ''), last_name),
            dept = COALESCE(NULLIF(%s, ''), dept),
            salary = COALESCE(NULLIF(%s, ''), salary),
            isDuke = COALESCE(NULLIF(%s, ''), isDuke)
        WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(update_query, (
                new_first_name[0] if new_first_name else None,
                new_last_name[0] if new_last_name else None,
                new_dept if new_dept else None,
                new_salary[0] if new_salary and new_salary[0].isdigit() else None,
                is_duke[0].lower() == "yes" if is_duke else None,
                instructor_id
            ))
            printToScreen("Instructor information updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update instructor: {e}")


    def insert_instructor(self):
        id = getUserInput("Enter new instructor ID:")
        first_name = getUserInput("Enter first name:")
        last_name = getUserInput("Enter last name:")
        
        dept_query = "SELECT name FROM dept"
        departments = self.session.db_connection.execute_query(dept_query)
        if not departments:
            printToScreen("No departments found. Cannot add instructor.")
            return

        printToScreen("Available departments:")
        for idx, department in enumerate(departments):
            printToScreen(f"{idx + 1}. {department['name']}")

        dept_index = getUserInput("Select the department by number (or press ENTER to cancel):")
        if not dept_index or not dept_index[0].isdigit():
            printToScreen("Operation canceled.")
            return

        dept_index = int(dept_index[0]) - 1
        if dept_index < 0 or dept_index >= len(departments):
            printToScreen("Invalid selection. Operation canceled.")
            return

        dept = departments[dept_index]['name']

        salary = getUserInput("Enter salary:")
        is_duke = getUserInput("Is this instructor a Duke employee? (1 for yes/0 for no):")

        insert_query = """
        INSERT INTO instructor (id, first_name, last_name, dept, salary, isDuke)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.session.db_connection.execute_update(insert_query, (
                id[0], first_name[0], last_name[0], dept,
                salary[0] if salary[0].isdigit() else None,
                int(is_duke[0]) if is_duke and is_duke[0] in ["1", "0"] else None
            ))
            printToScreen("Instructor added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add instructor: {e}")

    def delete_instructor(self):
        first_name = getUserInput("Enter the instructor's first name (or press ENTER to skip):")
        last_name = getUserInput("Enter the instructor's last name (or press ENTER to skip):")
        
        search_query = """
        SELECT id, first_name, last_name, dept, salary, isDuke
        FROM instructor
        WHERE first_name LIKE %s AND last_name LIKE %s
        """
        search_results = self.session.db_connection.execute_query(
            search_query, 
            (f"%{first_name[0]}%" if first_name else "%", f"%{last_name[0]}%" if last_name else "%")
        )

        if not search_results:
            printToScreen("No instructors found with the given search criteria.")
            return

        printToScreen("Instructors found:")
        for idx, instructor in enumerate(search_results):
            printToScreen(f"{idx + 1}. ID: {instructor['id']}, Name: {instructor['first_name']} {instructor['last_name']}, "
                        f"Department: {instructor['dept']}, Salary: {instructor['salary']}, Duke Status: {instructor['isDuke']}")

        selected_index = getUserInput("Enter the number of the instructor to delete (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Deletion canceled.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(search_results):
            printToScreen("Invalid selection. Deletion canceled.")
            return

        instructor_id = search_results[selected_index]['id']

        confirm = getUserInput(f"Are you sure you want to delete instructor ID {instructor_id}? (yes/no):")
        if confirm and confirm[0].lower() == "yes":
            delete_query = """
            DELETE FROM instructor
            WHERE id = %s
            """
            try:
                self.session.db_connection.execute_update(delete_query, (instructor_id,))
                printToScreen("Instructor deleted successfully.")
            except Exception as e:
                printToScreen(f"Failed to delete instructor: {e}")
        else:
            printToScreen("Deletion canceled.")



class ManageDepartmentScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Department Management:\n")

    def prompt(self):
        options = [
            "View Departments",
            "Add New Department",
            "Modify Department",
            "Delete Department",
            "Return to Admin Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  
            self.view_departments()
        elif user_choice[0] == "1":  
            self.add_department()
        elif user_choice[0] == "2":  
            self.modify_department()
        elif user_choice[0] == "3":  
            self.delete_department()
        elif user_choice[0] == "4":  
            return ScreenType.ADMIN, ()

        return ScreenType.MANAGE_DEPARTMENT, ()

    def view_departments(self):
        printToScreen("View Departments")

        query = "SELECT name, budget FROM dept"
        departments = self.session.db_connection.execute_query(query)

        if not departments:
            printToScreen("No departments found.")
            return

        printToScreen("Departments:")
        for dept in departments:
            printToScreen(f"Name: {dept['name']}, Budget: {dept['budget']}")

    def add_department(self):
        printToScreen("Add New Department")

        dept_name = getUserInput("Enter department name:")
        budget = getUserInput("Enter department budget:")
        dept_name = " ".join(dept_name) if dept_name else None

        if not dept_name or not dept_name[0] or not budget or not budget[0].isdigit():
            printToScreen("Invalid inputs. Please provide a valid department name and budget.")
            return

        insert_query = "INSERT INTO dept (name, budget) VALUES (%s, %s)"
        try:
            self.session.db_connection.execute_update(insert_query, (dept_name, int(budget[0])))
            printToScreen("Department added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add department: {e}")

    def modify_department(self):
        printToScreen("Modify Department")

        dept_name = getUserInput("Enter the department name to modify:")
        dept_name = " ".join(dept_name) if dept_name else None
        if not dept_name or not dept_name[0]:
            printToScreen("Department name is required.")
            return

        query = "SELECT name, budget FROM dept WHERE name = %s"
        department = self.session.db_connection.execute_query(query, (dept_name,))
        if not department:
            printToScreen("Department not found.")
            return

        new_name = getUserInput("Enter new department name (or press ENTER to keep current):")
        new_budget = getUserInput("Enter new budget (or press ENTER to keep current):")

        update_query = """
        UPDATE dept
        SET name = COALESCE(NULLIF(%s, ''), name),
            budget = COALESCE(NULLIF(%s, ''), budget)
        WHERE name = %s
        """
        try:
            self.session.db_connection.execute_update(update_query, (
                new_name[0] if new_name else None,
                int(new_budget[0]) if new_budget and new_budget[0].isdigit() else None,
                dept_name[0]
            ))
            printToScreen("Department updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update department: {e}")

    def delete_department(self):
        printToScreen("Delete Department")

        dept_name = getUserInput("Enter the department name to delete:")
        dept_name = " ".join(dept_name) if dept_name else None
        if not dept_name or not dept_name[0]:
            printToScreen("Department name is required.")
            return

        confirm = getUserInput(f"Are you sure you want to delete department '{dept_name}'? (yes/no):")
        if not confirm or confirm[0].lower() != "yes":
            printToScreen("Department deletion canceled.")
            return

        delete_query = "DELETE FROM dept WHERE name = %s"
        try:
            self.session.db_connection.execute_update(delete_query, (dept_name,))
            printToScreen("Department deleted successfully.")
        except Exception as e:
            printToScreen(f"Failed to delete department: {e}")

class ManageStudentScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Student Management:\n")

    def prompt(self):
        options = [
            "View Students",
            "Add New Student",
            "Modify Student",
            "Delete Student",
            "Add Advising Holds to All Students",
            "Add Registrar Holds to All Students",
            "Return to Admin Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0": 
            self.view_students()
        elif user_choice[0] == "1": 
            self.add_student()
        elif user_choice[0] == "2":  
            self.modify_student()
        elif user_choice[0] == "3":  
            self.delete_student()
        elif user_choice[0] == "4":  
            self.session.db_connection.execute_procedure("AddAdvisingHoldsToAllStudents", ())
            printToScreen("Successfully added advising holds to all students.")
        elif user_choice[0] == "5":  
            self.session.db_connection.execute_procedure("AddRegistrarHoldsToAllStudents", ())
            printToScreen("Successfully added registrar holds to all students.")
        elif user_choice[0] == "6":  
            return ScreenType.ADMIN, ()

        return ScreenType.MANAGE_STUDENT, ()

    def view_students(self):
        printToScreen("View Students")

        student_id = getUserInput("Enter student ID (or press ENTER to skip):")
        
        query = """
        SELECT id, first_name, last_name, major, class
        FROM student
        WHERE id LIKE %s
        """
        params = (
            f"%{student_id[0]}%" if student_id else "%",
        )

        students = self.session.db_connection.execute_query(query, params)

        if not students:
            printToScreen("No students found matching the criteria.")
            return

        printToScreen("Matching Students:")
        for student in students:
            printToScreen(
                f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, "
                f"Major: {student['major']}, Class: {student['class']}"
            )

    def add_student(self):
        printToScreen("Add New Student")

        student_id = getUserInput("Enter student ID:")
        first_name = getUserInput("Enter first name:")
        last_name = getUserInput("Enter last name:")
        year = getUserInput("Enter academic year:")
        major = self.select_major() or 'Not Declared'

        insert_query = """
        INSERT INTO student (id, first_name, last_name, class, major)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.session.db_connection.execute_update(insert_query, (
                student_id[0], first_name[0], last_name[0],
                year[0] if year else None,
                major
            ))
            printToScreen("Student added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add student: {e}")

    def modify_student(self):
        printToScreen("Modify Student")
        student_id = getUserInput("Enter student ID to modify:")
        if not student_id or not student_id[0]:
            printToScreen("Student ID is required.")
            return

        query = """
        SELECT id, first_name, last_name, class, major
        FROM student
        WHERE id = %s
        """
        student = self.session.db_connection.execute_query(query, (student_id[0],))
        if not student:
            printToScreen("Student not found.")
            return

        student = student[0]  # Select the first (and only) result
        new_first_name = getUserInput("Enter new first name (or press ENTER to keep current):")
        new_last_name = getUserInput("Enter new last name (or press ENTER to keep current):")
        new_year = getUserInput("Enter new academic year (or press ENTER to keep current):")
        new_major = self.select_major() or student['major']

        update_query = """
        UPDATE student
        SET first_name = COALESCE(NULLIF(%s, ''), first_name),
            last_name = COALESCE(NULLIF(%s, ''), last_name),
            class = COALESCE(NULLIF(%s, ''), class),
            major = COALESCE(NULLIF(%s, ''), major)
        WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(update_query, (
                new_first_name[0] if new_first_name else None,
                new_last_name[0] if new_last_name else None,
                new_year[0] if new_year else None,
                new_major,
                student_id[0]
            ))
            printToScreen("Student information updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update student: {e}")

    def delete_student(self):
        printToScreen("Delete Student")

        student_id = getUserInput("Enter student ID to delete:")
        if not student_id or not student_id[0]:
            printToScreen("Student ID is required.")
            return

        confirm = getUserInput(f"Are you sure you want to delete student ID {student_id[0]}? (yes/no):")
        if not confirm or confirm[0].lower() != "yes":
            printToScreen("Student deletion canceled.")
            return

        delete_query = """
        DELETE FROM student WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(delete_query, (student_id[0],))
            printToScreen("Student deleted successfully.")
        except Exception as e:
            printToScreen(f"Failed to delete student: {e}")

    def select_major(self):
        query = "SELECT name FROM major"
        majors = self.session.db_connection.execute_query(query)
        if not majors:
            printToScreen("No majors available. Please add majors first.")
            return None

        printToScreen("Available Majors:")
        for idx, major in enumerate(majors):
            printToScreen(f"{idx + 1}. {major['name']}")

        major_index = getUserInput("Select the major by number (or press ENTER to skip):")
        if not major_index or not major_index[0].isdigit():
            return None

        major_index = int(major_index[0]) - 1
        if major_index < 0 or major_index >= len(majors):
            printToScreen("Invalid selection.")
            return None

        return majors[major_index]['name']



class ManageCourseScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Manage Courses and Sections")
        
    def prompt(self):
        options = ["Manage Courses", "Add New Course", "Delete Course", "Manage Sections", "Return to Home"]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Manage Courses
            self.manage_courses()
        elif user_choice[0] == "1":  # Add New Course
            self.add_course()
        elif user_choice[0] == "2":  # Delete Course
            self.delete_course()
        elif user_choice[0] == "3":  # Manage Sections (placeholder for now)
            self.manage_sections()
        else:
            return ScreenType.HOME, ()

    def manage_courses(self):
        course_id = getUserInput("Enter course ID:")
        course_id = " ".join(course_id) if course_id else None

        query = """
        SELECT c.id, c.name, c.type, c.dept_name, c.credits, c.description
        FROM course c
        WHERE c.id LIKE %s
        """
        courses = self.session.db_connection.execute_query(query, (f"%{course_id}%",))

        if not courses:
            printToScreen("No courses found with the given ID.")
            return

        printToScreen("Matching Courses:")
        for idx, course in enumerate(courses):
            printToScreen(
                f"{idx + 1}. ID: {course['id']}, Name: {course['name']}, Type: {course['type']}, "
                f"Department: {course['dept_name']}, Credits: {course['credits']}\n"
                f"   Description: {course['description']}"
            )

        selected_index = getUserInput("Enter the number of the course to modify (or press ENTER to return):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(courses):
            printToScreen("Invalid selection.")
            return

        selected_course = courses[selected_index]
        self.modify_course(selected_course['id'])

    def modify_course(self, course_id):
        printToScreen("Modify Course Information")
        
        new_name = getUserInput("Enter new course name (or press ENTER to skip):")
        new_type = getUserInput("Enter new course type (lec, sem, lab, rec) (or press ENTER to skip):")
        new_dept = self.select_department()
        new_credits = getUserInput("Enter new credits (or press ENTER to skip):")
        new_description = getUserInput("Enter new course description (or press ENTER to skip):")
        new_division = self.select_course_division()
        new_name = " ".join(new_name) if new_name else None
        new_description =  " ".join(new_description) if new_description else None

        update_query = """
        UPDATE course
        SET name = COALESCE(NULLIF(%s, ''), name),
            type = COALESCE(NULLIF(%s, ''), type),
            dept_name = COALESCE(NULLIF(%s, ''), dept_name),
            credits = COALESCE(NULLIF(%s, ''), credits),
            description = COALESCE(NULLIF(%s, ''), description)
        WHERE id LIKE %s
        """
        try:
            self.session.db_connection.execute_update(update_query, (
                new_name if new_name else None,
                new_type[0] if new_type else None,
                new_dept,
                new_credits[0] if new_credits and new_credits[0].isdigit() else None,
                new_description if new_description else None,
                course_id
            ))

            if new_division:
                division_query = """
                INSERT INTO course_division (course_id, division)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE division = VALUES(division)
                """
                self.session.db_connection.execute_update(division_query, (course_id, new_division))

            printToScreen("Course information updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update course: {e}")

    def add_course(self):
        printToScreen("Add New Course")

        course_id = getUserInput("Enter course ID:")
        course_name = getUserInput("Enter course name:")
        course_type = getUserInput("Enter course type (lec, sem, lab, rec):")
        course_dept = self.select_department()
        course_credits = getUserInput("Enter course credits:")
        course_description = getUserInput("Enter course description:")
        course_division = self.select_course_division()
        
        
        course_id = " ".join(course_id) if course_id else None
        course_name = " ".join(course_name) if course_name else None
        course_description =  " ".join(course_description) if course_description else None


        insert_query = """
        INSERT INTO course (id, name, type, dept_name, credits, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        division_query = """
        INSERT INTO course_division (course_id, division)
        VALUES (%s, %s)
        """

        try:
            self.session.db_connection.execute_update(insert_query, (
                course_id, course_name, course_type[0], course_dept,
                float(course_credits[0]) if course_credits and course_credits[0].isdigit() else 0.0,
                course_description
            ))

            if course_division:
                self.session.db_connection.execute_update(division_query, (course_id, course_division))

            printToScreen("Course added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add course: {e}")

    def delete_course(self):
        course_id = getUserInput("Enter course ID to delete:")
        course_id = " ".join(course_id) if course_id else None

        query = """
        SELECT c.id, c.name, c.type, c.dept_name, c.credits
        FROM course c
        WHERE c.id Like %s
        """
        courses = self.session.db_connection.execute_query(query, (f"%{course_id}%",))

        if not courses:
            printToScreen("No courses found with the given ID.")
            return

        printToScreen("Matching Courses:")
        for idx, course in enumerate(courses):
            printToScreen(
                f"{idx + 1}. ID: {course['id']}, Name: {course['name']}, Type: {course['type']}, "
                f"Department: {course['dept_name']}, Credits: {course['credits']}"
            )

        selected_index = getUserInput("Enter the number of the course to delete (or press ENTER to return):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(courses):
            printToScreen("Invalid selection.")
            return

        selected_course = courses[selected_index]

        confirm = getUserInput(f"Are you sure you want to delete course '{selected_course['name']}'? (yes/no):")
        if not confirm or confirm[0].lower() != "yes":
            printToScreen("Course deletion canceled.")
            return

        delete_query = """
        DELETE FROM course WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(delete_query, (selected_course['id'],))
            printToScreen("Course deleted successfully.")
        except Exception as e:
            printToScreen(f"Failed to delete course: {e}")

    def select_department(self):
        query = "SELECT name FROM dept"
        departments = self.session.db_connection.execute_query(query)
        if not departments:
            printToScreen("No departments found.")
            return None

        printToScreen("Available departments:")
        for idx, dept in enumerate(departments):
            printToScreen(f"{idx + 1}. {dept['name']}")

        dept_index = getUserInput("Select the department by number (or press ENTER to skip):")
        if not dept_index or not dept_index[0].isdigit():
            return None

        dept_index = int(dept_index[0]) - 1
        if dept_index < 0 or dept_index >= len(departments):
            printToScreen("Invalid selection.")
            return None

        return departments[dept_index]['name']

    def select_course_division(self):
        divisions = ["Art and Humanity", "Natural Science", "Social Science"]
        printToScreen("Available Course Divisions:")
        for idx, division in enumerate(divisions):
            printToScreen(f"{idx + 1}. {division}")

        division_index = getUserInput("Select the course division by number (or press ENTER to skip):")
        if not division_index or not division_index[0].isdigit():
            return None

        division_index = int(division_index[0]) - 1
        if division_index < 0 or division_index >= len(divisions):
            printToScreen("Invalid selection.")
            return None

        return divisions[division_index]
    
    def manage_sections(self):
        printToScreen("Manage Sections")
        options = [
            "View Sections",
            "Add New Section",
            "Modify Section",
            "Delete Section",
            "Assign Instructor to Section",
            "Return to Course Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # View Sections
            self.view_sections()
        elif user_choice[0] == "1":  # Add New Section
            self.add_section()
        elif user_choice[0] == "2":  # Modify Section
            self.modify_section()
        elif user_choice[0] == "4":  # Assign Instructor to Section
            self.assign_instructor_to_section()
        else:
            return ScreenType.HOME, ()
    
    def assign_instructor_to_section(self):
        printToScreen("Assign Instructor to Section")

        course_id = getUserInput("Enter course ID (or press ENTER to skip):")
        year = getUserInput("Enter year (or press ENTER to skip):")
        term = getUserInput("Enter term (spring, fall, summer) (or press ENTER to skip):")
        course_id = " ".join(course_id) if course_id else None

        query = """
        SELECT DISTINCT 
            s.id AS section_id, 
            s.course_id, 
            s.type, 
            s.term, 
            s.session, 
            s.year, 
            s.capacity, 
            s.building_name, 
            s.room_name, 
            c.name AS course_name
        FROM section s
        INNER JOIN course c ON s.course_id = c.id
        WHERE 1=1
        """

        params = []

        if course_id:
            query += " AND s.course_id = %s"
            params.append(course_id)

        if year and year[0].isdigit():
            query += " AND s.year = %s"
            params.append(int(year[0]))

        if term and term[0].lower() in ['spring', 'fall', 'summer']:
            query += " AND s.term = %s"
            params.append(term[0].lower())

        sections = self.session.db_connection.execute_query(query, params)

        if not sections:
            printToScreen("No sections found matching the criteria.")
            return

        printToScreen("Matching Sections:")
        for idx, section in enumerate(sections):
            printToScreen(
                f"{idx + 1}. Section ID: {section['section_id']}, Course Name: {section['course_name']}, "
                f"Type: {section['type']}, Term: {section['term']}, "
                f"Session: {section['session']}, Year: {section['year']}, Capacity: {section['capacity']}, "
                f"Building: {section['building_name']}, Room: {section['room_name']}"
            )

        selected_index = getUserInput("Enter the number of the section to assign an instructor (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(sections):
            printToScreen("Invalid selection.")
            return

        selected_section = sections[selected_index]

        query = """
        SELECT id, first_name, last_name, dept, salary, isDuke
        FROM instructor
        """
        instructors = self.session.db_connection.execute_query(query)

        if not instructors:
            printToScreen("No instructors available.")
            return

        printToScreen("Available Instructors:")
        for idx, instructor in enumerate(instructors):
            printToScreen(
                f"{idx + 1}. ID: {instructor['id']}, Name: {instructor['first_name']} {instructor['last_name']}, "
                f"Department: {instructor['dept']}, Salary: {instructor['salary']}, Duke Status: {instructor['isDuke']}"
            )

        selected_index = getUserInput("Enter the number of the instructor to assign (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(instructors):
            printToScreen("Invalid selection.")
            return

        selected_instructor = instructors[selected_index]

        try:
            assign_query = """
            INSERT INTO teaches (instructor_id, section_id)
            VALUES (%s, %s)
            """
            self.session.db_connection.execute_update(assign_query, (selected_instructor['id'], selected_section['section_id']))
            printToScreen(f"Instructor {selected_instructor['first_name']} {selected_instructor['last_name']} "
                        f"has been successfully assigned to section {selected_section['section_id']} "
                        f"of course {selected_section['course_name']}.")
        except Exception as e:
            printToScreen(f"Failed to assign instructor: {e}")


    def view_sections(self):
        printToScreen("View Sections")

        course_id = getUserInput("Enter course ID (or press ENTER to skip):")
        year = getUserInput("Enter year (or press ENTER to skip):")
        term = getUserInput("Enter term (spring, fall, summer) (or press ENTER to skip):")
        
        course_id = " ".join(course_id) if course_id else None
        query = """
        SELECT s.id, s.course_id, s.type, s.term, s.session, s.year, s.capacity, s.building_name, s.room_name
        FROM section s
        WHERE 1=1
        """
        params = []

        if course_id and course_id:
            query += " AND s.course_id = %s"
            params.append(course_id)

        if year and year[0].isdigit():
            query += " AND s.year = %s"
            params.append(int(year[0]))

        if term and term[0].lower() in ['spring', 'fall', 'summer']:
            query += " AND s.term = %s"
            params.append(term[0].lower())

        sections = self.session.db_connection.execute_query(query, params)

        if not sections:
            printToScreen("No sections found matching the criteria.")
            return

        printToScreen("Matching Sections:")
        for section in sections:
            printToScreen(
                    f"Course ID: {section['course_id']}, Section ID: {section['id']}, Type: {section['type']}, Term: {section['term']}, "
                f"Session: {section['session']}, Year: {section['year']}, Capacity: {section['capacity']}, "
                f"Building: {section['building_name']}, Room: {section['room_name']}"
            )


    def add_section(self):
        printToScreen("Add New Section")
        course_id = getUserInput("Enter course ID:")
        section_type = getUserInput("Enter section type (lec, sem, lab, rec):")
        term = getUserInput("Enter term (spring, fall, summer):")
        session = getUserInput("Enter session (first, second, mini, semester):")
        year = getUserInput("Enter year:")
        capacity = getUserInput("Enter section capacity:")
        building_name = self.select_building()
        room_name = self.select_room(building_name) if building_name else None
        course_id = " ".join(course_id) if course_id else None

        time_slots = [
            {"id": 1, "start_time": "08:30:00", "end_time": "09:45:00"},
            {"id": 2, "start_time": "08:30:00", "end_time": "11:00:00"},
            {"id": 3, "start_time": "10:00:00", "end_time": "11:15:00"},
            {"id": 4, "start_time": "11:45:00", "end_time": "13:00:00"},
            {"id": 5, "start_time": "12:00:00", "end_time": "14:30:00"},
            {"id": 6, "start_time": "13:15:00", "end_time": "14:30:00"},
            {"id": 7, "start_time": "14:45:00", "end_time": "16:00:00"},
            {"id": 8, "start_time": "14:45:00", "end_time": "17:15:00"},
            {"id": 9, "start_time": "16:15:00", "end_time": "17:30:00"},
            {"id": 10, "start_time": "18:00:00", "end_time": "19:15:00"},
            {"id": 11, "start_time": "19:15:00", "end_time": "20:15:00"},
            {"id": 12, "start_time": "20:30:00", "end_time": "22:00:00"},
        ]

        printToScreen("Available Time Slots:")
        for slot in time_slots:
            printToScreen(f"{slot['id']}. {slot['start_time']} - {slot['end_time']}")

        selected_time_slot_id = getUserInput("Select a time slot by ID:")
        if not selected_time_slot_id or not selected_time_slot_id[0].isdigit():
            printToScreen("Invalid selection. Time slot selection is required.")
            return

        selected_time_slot_id = int(selected_time_slot_id[0])
        if selected_time_slot_id < 1 or selected_time_slot_id > len(time_slots):
            printToScreen("Invalid time slot ID. Please try again.")
            return


        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
        printToScreen("Available Days:")
        for idx, day in enumerate(days, start=1):
            printToScreen(f"{idx}. {day.capitalize()}")

        selected_day_id = getUserInput("Select a day by number:")
        if not selected_day_id or not selected_day_id[0].isdigit():
            printToScreen("Invalid selection. Day selection is required.")
            return

        selected_day_id = int(selected_day_id[0])
        if selected_day_id < 1 or selected_day_id > len(days):
            printToScreen("Invalid day selection. Please try again.")
            return

        day = days[selected_day_id - 1]

        try:
            section_query = """
            INSERT INTO section (course_id, type, term, session, year, capacity, building_name, room_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.db_connection.execute_update(section_query, (
                course_id, section_type[0], term[0], session[0],
                int(year[0]), int(capacity[0]),
                building_name, room_name
            ))


            section_id_query = "SELECT LAST_INSERT_ID() AS section_id"
            section_id_result = self.session.db_connection.execute_query(section_id_query)
            if not section_id_result or not section_id_result[0].get("section_id"):
                raise ValueError("Failed to retrieve section_id after insert.")

            section_id = section_id_result[0]["section_id"]

            section_time_query = """
            INSERT INTO section_time (section_id, time_slot_id, day)
            VALUES (%s, %s, %s)
            """
            self.session.db_connection.execute_update(section_time_query, (section_id, selected_time_slot_id, day))

            printToScreen("Section added successfully with the selected time slot and day.")
        except Exception as e:
            printToScreen(f"Failed to add section: {e}")


    def modify_section(self):
        printToScreen("Modify Section")

        course_id = getUserInput("Enter course ID (or press ENTER to skip):")
        year = getUserInput("Enter year (or press ENTER to skip):")
        term = getUserInput("Enter term (spring, fall, summer) (or press ENTER to skip):")
        course_id = " ".join(course_id).strip() if course_id else None

        query = """
        SELECT s.id, s.course_id, s.type, s.term, s.session, s.year, s.capacity, s.building_name, s.room_name
        FROM section s
        WHERE 1=1
        """
        params = []

        if course_id:
            query += " AND s.course_id = %s"
            params.append(course_id)

        if year and year[0].isdigit():
            query += " AND s.year = %s"
            params.append(int(year[0]))

        if term and term[0].lower() in ['spring', 'fall', 'summer']:
            query += " AND s.term = %s"
            params.append(term[0].lower())

        sections = self.session.db_connection.execute_query(query, params)

        if not sections:
            printToScreen("No sections found matching the criteria.")
            return

        printToScreen("Matching Sections:")
        for idx, section in enumerate(sections):
            printToScreen(
                f"{idx + 1}. ID: {section['id']}, Type: {section['type']}, Term: {section['term']}, "
                f"Session: {section['session']}, Year: {section['year']}, Capacity: {section['capacity']}, "
                f"Building: {section['building_name']}, Room: {section['room_name']}"
            )

        selected_index = getUserInput("Enter the number of the section to modify (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(sections):
            printToScreen("Invalid selection.")
            return

        selected_section = sections[selected_index]

        printToScreen(f"Updating Section ID: {selected_section['id']}")
        new_capacity = getUserInput(f"Enter new capacity (current: {selected_section['capacity']}, or press ENTER to keep):")
        new_building = self.select_building() or selected_section['building_name']
        new_room = self.select_room(new_building) if new_building != selected_section['building_name'] else selected_section['room_name']

        time_slots = [
            {"id": 1, "start_time": "08:30:00", "end_time": "09:45:00"},
            {"id": 2, "start_time": "08:30:00", "end_time": "11:00:00"},
            {"id": 3, "start_time": "10:00:00", "end_time": "11:15:00"},
            {"id": 4, "start_time": "11:45:00", "end_time": "13:00:00"},
            {"id": 5, "start_time": "12:00:00", "end_time": "14:30:00"},
            {"id": 6, "start_time": "13:15:00", "end_time": "14:30:00"},
            {"id": 7, "start_time": "14:45:00", "end_time": "16:00:00"},
            {"id": 8, "start_time": "14:45:00", "end_time": "17:15:00"},
            {"id": 9, "start_time": "16:15:00", "end_time": "17:30:00"},
            {"id": 10, "start_time": "18:00:00", "end_time": "19:15:00"},
            {"id": 11, "start_time": "19:15:00", "end_time": "20:15:00"},
            {"id": 12, "start_time": "20:30:00", "end_time": "22:00:00"},
        ]

        printToScreen("Available Time Slots:")
        for slot in time_slots:
            printToScreen(f"{slot['id']}. {slot['start_time']} - {slot['end_time']}")

        selected_time_slot_id = getUserInput("Select a new time slot by ID (or press ENTER to keep current):")
        if selected_time_slot_id and selected_time_slot_id[0].isdigit():
            selected_time_slot_id = int(selected_time_slot_id[0])
            if selected_time_slot_id < 1 or selected_time_slot_id > len(time_slots):
                printToScreen("Invalid time slot ID. Keeping current.")
                selected_time_slot_id = None
        else:
            selected_time_slot_id = None

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        printToScreen("Available Days:")
        for idx, day in enumerate(days, start=1):
            printToScreen(f"{idx}. {day.capitalize()}")

        selected_day_id = getUserInput("Select a new day by number (or press ENTER to keep current):")
        if selected_day_id and selected_day_id[0].isdigit():
            selected_day_id = int(selected_day_id[0])
            if selected_day_id < 1 or selected_day_id > len(days):
                printToScreen("Invalid day selection. Keeping current.")
                selected_day_id = None
        else:
            selected_day_id = None

        try:

            update_section_query = """
            UPDATE section
            SET capacity = %s, building_name = %s, room_name = %s
            WHERE id = %s
            """
            self.session.db_connection.execute_update(update_section_query, (
                int(new_capacity[0]) if new_capacity and new_capacity[0].isdigit() else selected_section['capacity'],
                new_building, new_room, selected_section['id']
            ))

            if selected_time_slot_id or selected_day_id:
                update_section_time_query = """
                UPDATE section_time
                SET time_slot_id = %s, day = %s
                WHERE section_id = %s
                """
                self.session.db_connection.execute_update(update_section_time_query, (
                    selected_time_slot_id or selected_section['time_slot_id'],
                    days[selected_day_id - 1] if selected_day_id else selected_section['day'],
                    selected_section['id']
                ))

            printToScreen("Section updated successfully.")
        except Exception as e:
            printToScreen(f"Failed to update section: {e}")


    def delete_section(self):
        printToScreen("Delete Section")

        course_id = getUserInput("Enter course ID (or press ENTER to skip):")
        year = getUserInput("Enter year (or press ENTER to skip):")
        term = getUserInput("Enter term (spring, fall, summer) (or press ENTER to skip):")
        course_id = " ".join(course_id) if course_id else None
        query = """
        SELECT s.id, s.course_id, s.type, s.term, s.session, s.year, s.capacity, s.building_name, s.room_name
        FROM section s
        WHERE 1=1
        """
        params = []

        if course_id and course_id:
            query += " AND s.course_id = %s"
            params.append(course_id)

        if year and year[0].isdigit():
            query += " AND s.year = %s"
            params.append(int(year[0]))

        if term and term[0].lower() in ['spring', 'fall', 'summer']:
            query += " AND s.term = %s"
            params.append(term[0].lower())

        sections = self.session.db_connection.execute_query(query, params)

        if not sections:
            printToScreen("No sections found matching the criteria.")
            return

        printToScreen("Matching Sections:")
        for idx, section in enumerate(sections):
            printToScreen(
                f"{idx + 1}. ID: {section['id']}, Type: {section['type']}, Term: {section['term']}, "
                f"Session: {section['session']}, Year: {section['year']}, Capacity: {section['capacity']}, "
                f"Building: {section['building_name']}, Room: {section['room_name']}"
            )


        selected_index = getUserInput("Enter the number of the section to delete (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(sections):
            printToScreen("Invalid selection.")
            return

        selected_section = sections[selected_index]

  
        confirm = getUserInput(f"Are you sure you want to delete section ID {selected_section['id']}? (yes/no):")
        if not confirm or confirm[0].lower() != "yes":
            printToScreen("Section deletion canceled.")
            return

        delete_query = """
        DELETE FROM section WHERE id = %s
        """
        try:
            self.session.db_connection.execute_update(delete_query, (selected_section['id'],))
            printToScreen("Section deleted successfully.")
        except Exception as e:
            printToScreen(f"Failed to delete section: {e}")

    def select_building(self):
        query = "SELECT name FROM building"
        buildings = self.session.db_connection.execute_query(query)
        if not buildings:
            printToScreen("No buildings found.")
            return None

        printToScreen("Available buildings:")
        for idx, building in enumerate(buildings):
            printToScreen(f"{idx + 1}. {building['name']}")

        building_index = getUserInput("Select the building by number (or press ENTER to skip):")
        if not building_index or not building_index[0].isdigit():
            return None

        building_index = int(building_index[0]) - 1
        if building_index < 0 or building_index >= len(buildings):
            printToScreen("Invalid selection.")
            return None

        return buildings[building_index]['name']

    def select_room(self, building_name):
        query = "SELECT room_name FROM classroom WHERE building_name = %s"
        rooms = self.session.db_connection.execute_query(query, (building_name,))
        if not rooms:
            printToScreen(f"No rooms found for building '{building_name}'.")
            return None

        printToScreen("Available rooms:")
        for idx, room in enumerate(rooms):
            printToScreen(f"{idx + 1}. {room['room_name']}")

        room_index = getUserInput("Select the room by number (or press ENTER to skip):")
        if not room_index or not room_index[0].isdigit():
            return None

        room_index = int(room_index[0]) - 1
        if room_index < 0 or room_index >= len(rooms):
            printToScreen("Invalid selection.")
            return None

        return rooms[room_index]['room_name']


class StatisticsScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Statistics Dashboard:\n")

    def prompt(self):
        options = [
            "Student Statistics",
            "Instructor Statistics",
            "Course Statistics",
            "Return to Admin Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Student Statistics
            return ScreenType.STUDENT_STATS, ()
        elif user_choice[0] == "1":  # Instructor Statistics
            return ScreenType.INSTRUCTOR_STATS, ()
        elif user_choice[0] == "2":  # Course Statistics
            return ScreenType.COURSE_STATS, ()
        elif user_choice[0] == "3":  # Return to Admin Menu
            return ScreenType.ADMIN, ()

        return ScreenType.STATISTICS, ()


class StudentStatisticsScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Student Statistics:\n")

    def prompt(self):
        options = [
            "View Number of Students by Class",
            "View GPA Distribution",
            "Return to Statistics Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Students by Class
            self.view_students_by_class()
        elif user_choice[0] == "1":  # GPA Distribution
            self.view_gpa_distribution()
        elif user_choice[0] == "2":  # Return to Statistics Menu
            return ScreenType.STATISTICS, ()

        return ScreenType.STUDENT_STATS, ()

    def view_students_by_class(self):
        query = """
        SELECT class, COUNT(*) as student_count
        FROM student
        GROUP BY class
        ORDER BY class
        """
        results = self.session.db_connection.execute_query(query)

        printToScreen("Number of Students by Class:")
        for row in results:
            printToScreen(f"Class: {row['class']}, Students: {row['student_count']}")

    def view_gpa_distribution(self):
        query = """
        SELECT grade, COUNT(*) as count
        FROM enrollment
        GROUP BY grade
        ORDER BY FIELD(grade, 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NC', 'CR')
        """
        results = self.session.db_connection.execute_query(query)

        printToScreen("GPA Distribution:")
        for row in results:
            printToScreen(f"Grade: {row['grade']}, Count: {row['count']}")


class InstructorStatisticsScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Instructor Statistics:\n")

    def prompt(self):
        options = [
            "View Average Salary by Department",
            "View Instructor Count by Department",
            "Return to Statistics Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Average Salary by Department
            self.view_avg_salary_by_dept()
        elif user_choice[0] == "1":  # Instructor Count by Department
            self.view_instructor_count_by_dept()
        elif user_choice[0] == "2":  # Return to Statistics Menu
            return ScreenType.STATISTICS, ()

        return ScreenType.INSTRUCTOR_STATS, ()

    def view_avg_salary_by_dept(self):
        query = """
        SELECT dept, AVG(salary) as avg_salary
        FROM instructor
        GROUP BY dept
        """
        results = self.session.db_connection.execute_query(query)

        printToScreen("Average Salary by Department:")
        for row in results:
            printToScreen(f"Department: {row['dept']}, Average Salary: ${row['avg_salary']:.2f}")

    def view_instructor_count_by_dept(self):
        query = """
        SELECT dept, COUNT(*) as instructor_count
        FROM instructor
        GROUP BY dept
        """
        results = self.session.db_connection.execute_query(query)

        printToScreen("Instructor Count by Department:")
        for row in results:
            printToScreen(f"Department: {row['dept']}, Count: {row['instructor_count']}")


class CourseStatisticsScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Course Statistics:\n")

    def prompt(self):
        options = [
            "View Courses by Division",
            "Return to Statistics Menu"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Courses by Division
            self.view_courses_by_division()
        elif user_choice[0] == "1":  # Return to Statistics Menu
            return ScreenType.STATISTICS, ()

        return ScreenType.COURSE_STATS, ()

    def view_courses_by_division(self):
        query = """
        SELECT cd.division, COUNT(*) as course_count
        FROM course_division cd
        GROUP BY cd.division
        """
        results = self.session.db_connection.execute_query(query)

        printToScreen("Courses by Division:")
        for row in results:
            printToScreen(f"Division: {row['division']}, Courses: {row['course_count']}")
