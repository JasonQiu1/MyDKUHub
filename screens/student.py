# Screens just for students.

import plotext as plt

from screens.base import *
from screens.ui import *
from screens.types import *
from screens.types import *

from db.utils import *

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
