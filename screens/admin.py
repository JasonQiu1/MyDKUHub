from screens.base import *
from screens.ui import *
from screens.types import *

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
            "Return to Home Screen"
        ]
        user_choice = promptOptions(options)

        if user_choice[0] == "0":  # Manage Instructors
            return ScreenType.MANAGE_INSTRUCTOR, ()
        elif user_choice[0] == "1":  # Manage Departments
            return ScreenType.MANAGE_DEPARTMENT, ()
        elif user_choice[0] == "2":  # Manage Students
            return ScreenType.MANAGE_STUDENT, ()
        elif user_choice[0] == "3":  # Manage Courses
            return ScreenType.MANAGE_COURSE, ()
        elif user_choice[0] == "4":
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

        if user_choice[0] == "0":  # Search and Modify Instructor
            self.search_and_modify_instructor()
        elif user_choice[0] == "1":  # Insert New Instructor
            self.insert_instructor()
        elif user_choice[0] == "2":  # Delete Instructor
            self.delete_instructor()
        elif user_choice[0] == "3":  # Return to Admin Menu
            return ScreenType.ADMIN, ()

        return ScreenType.MANAGE_INSTRUCTOR, ()

    def search_and_modify_instructor(self):
        # Prompt for first and last name with the option to leave them blank
        first_name = getUserInput("Enter the instructor's first name (or leave empty for all):")
        last_name = getUserInput("Enter the instructor's last name (or leave empty for all):")

        # Handle blank inputs for flexible search
        first_name_filter = f"%{first_name[0]}%" if first_name else "%"
        last_name_filter = f"%{last_name[0]}%" if last_name else "%"

        query = """
        SELECT id, first_name, last_name, dept, salary, isDuke
        FROM instructor
        WHERE first_name LIKE %s AND last_name LIKE %s
        """
        results = self.session.db_connection.execute_query(query, (first_name_filter, last_name_filter))

        # Check if results were found
        if not results:
            printToScreen("No instructors found matching the criteria.")
            return

        # Display found instructors
        printToScreen("Instructors found:")
        for idx, instructor in enumerate(results):
            printToScreen(f"{idx + 1}. ID: {instructor['id']}, Name: {instructor['first_name']} {instructor['last_name']}, "
                        f"Department: {instructor['dept']}, Salary: {instructor['salary']}, Duke Status: {instructor['isDuke']}")

        # Allow user to select an instructor for modification
        selected_index = getUserInput("Enter the number of the instructor to modify (or press ENTER to return):")
        if not selected_index or not selected_index[0].isdigit():
            return

        # Validate selection
        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(results):
            printToScreen("Invalid selection.")
            return

        selected_instructor = results[selected_index]
        self.modify_instructor(selected_instructor['id'])


    def modify_instructor(self, instructor_id):
        # Prompt for new values
        new_first_name = getUserInput("Enter new first name (or press ENTER to skip):")
        new_last_name = getUserInput("Enter new last name (or press ENTER to skip):")

        # Fetch all valid departments
        dept_query = "SELECT name FROM dept"
        departments = self.session.db_connection.execute_query(dept_query)
        if not departments:
            printToScreen("No departments found. Please add departments first.")
            return

        # Display department options
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

        # Update query with COALESCE for nullable inputs
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
            # Execute update query
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
        # Prompt user for instructor details
        id = getUserInput("Enter new instructor ID:")
        first_name = getUserInput("Enter first name:")
        last_name = getUserInput("Enter last name:")
        
        # Retrieve and display all departments for selection
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

        # Continue with the rest of the details
        salary = getUserInput("Enter salary:")
        is_duke = getUserInput("Is this instructor a Duke employee? (1 for yes/0 for no):")

        # Insert the instructor into the database
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
        # Prompt for search criteria
        first_name = getUserInput("Enter the instructor's first name (or press ENTER to skip):")
        last_name = getUserInput("Enter the instructor's last name (or press ENTER to skip):")
        
        # Query to search for instructors based on first and last names
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

        # Display the search results
        printToScreen("Instructors found:")
        for idx, instructor in enumerate(search_results):
            printToScreen(f"{idx + 1}. ID: {instructor['id']}, Name: {instructor['first_name']} {instructor['last_name']}, "
                        f"Department: {instructor['dept']}, Salary: {instructor['salary']}, Duke Status: {instructor['isDuke']}")

        # Prompt user to select an instructor to delete
        selected_index = getUserInput("Enter the number of the instructor to delete (or press ENTER to cancel):")
        if not selected_index or not selected_index[0].isdigit():
            printToScreen("Deletion canceled.")
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(search_results):
            printToScreen("Invalid selection. Deletion canceled.")
            return

        instructor_id = search_results[selected_index]['id']

        # Confirm deletion
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
    def draw(self):
        printToScreen("Department Management:\n")
        # Placeholder: Display options or actions for managing departments.

    def prompt(self):
        # Placeholder for options such as Add, Remove, Update Departments.
        return ScreenType.ADMIN, ()

class ManageStudentScreen(Screen):
    def draw(self):
        printToScreen("Student Management:\n")
        # Placeholder: Display options or actions for managing students.

    def prompt(self):
        # Placeholder for options such as Add, Remove, Update Students.
        return ScreenType.ADMIN, ()

class ManageCourseScreen(Screen):
    def __init__(self, session):
        super().__init__(session)

    def draw(self):
        printToScreen("Manage Courses and Sections")
        self.prompt()

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
            printToScreen("Manage Sections is not implemented yet.")
        else:
            return ScreenType.HOME, ()

    def manage_courses(self):
        course_id = getUserInput("Enter course ID:")

        # Search for courses matching the input
        query = """
        SELECT c.id, c.name, c.type, c.dept_name, c.credits, c.description
        FROM course c
        WHERE c.id LIKE %s
        """
        courses = self.session.db_connection.execute_query(query, (f"%{course_id[0]}%",))

        if not courses:
            printToScreen("No courses found with the given ID.")
            return

        # Display matching courses
        printToScreen("Matching Courses:")
        for idx, course in enumerate(courses):
            printToScreen(
                f"{idx + 1}. ID: {course['id']}, Name: {course['name']}, Type: {course['type']}, "
                f"Department: {course['dept_name']}, Credits: {course['credits']}\n"
                f"   Description: {course['description']}"
            )

        # Prompt user to select a course for modification
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
        
        # Prompt for new values
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
        WHERE id = %s
        """
        try:
            # Update course table
            self.session.db_connection.execute_update(update_query, (
                new_name if new_name else None,
                new_type[0] if new_type else None,
                new_dept,
                new_credits[0] if new_credits and new_credits[0].isdigit() else None,
                new_description if new_description else None,
                course_id
            ))

            # Update course division
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

        # Prompt for course details
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
            # Insert course
            self.session.db_connection.execute_update(insert_query, (
                course_id, course_name, course_type[0], course_dept,
                float(course_credits[0]) if course_credits and course_credits[0].isdigit() else 0.0,
                course_description
            ))

            # Insert course division
            if course_division:
                self.session.db_connection.execute_update(division_query, (course_id, course_division))

            printToScreen("Course added successfully.")
        except Exception as e:
            printToScreen(f"Failed to add course: {e}")

    def delete_course(self):
        course_id = getUserInput("Enter course ID to delete:")

        # Search for courses matching the input
        query = """
        SELECT c.id, c.name, c.type, c.dept_name, c.credits
        FROM course c
        WHERE c.id LIKE %s
        """
        courses = self.session.db_connection.execute_query(query, (f"%{course_id[0]}%",))

        if not courses:
            printToScreen("No courses found with the given ID.")
            return

        # Display matching courses
        printToScreen("Matching Courses:")
        for idx, course in enumerate(courses):
            printToScreen(
                f"{idx + 1}. ID: {course['id']}, Name: {course['name']}, Type: {course['type']}, "
                f"Department: {course['dept_name']}, Credits: {course['credits']}"
            )

        # Prompt user to select a course to delete
        selected_index = getUserInput("Enter the number of the course to delete (or press ENTER to return):")
        if not selected_index or not selected_index[0].isdigit():
            return

        selected_index = int(selected_index[0]) - 1
        if selected_index < 0 or selected_index >= len(courses):
            printToScreen("Invalid selection.")
            return

        selected_course = courses[selected_index]

        # Confirm deletion
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
