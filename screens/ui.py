# All user interface functions for displaying information and receiving input.

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

def group_courses_by_course_id(courses):
    grouped_courses = {}
    for course in courses:
        course_id = course['course_id']
        if course_id not in grouped_courses:
            grouped_courses[course_id] = []
        grouped_courses[course_id].append(course)
    return grouped_courses

def display_courses(courses, instructor = True):
    grouped_courses = group_courses_by_course_id(courses)
    for idx, (course_id, course_group) in enumerate(grouped_courses.items()):
        printToScreen(f"{idx + 1}. {course_group[0]['year']} {course_group[0]['term']} {course_group[0]['session']} - "
                      f"{course_group[0]['course_id']} {course_group[0]['course_name']} - {course_group[0]['dept_name']}")
        for subcourse in course_group:
            if instructor:
                printToScreen(f"   - {subcourse['type']} (Section ID: {subcourse['section_id']}) - "
                            f"Instructor: {subcourse['instructor_first_name']} {subcourse['instructor_last_name']} - "
                            f"{subcourse['credits']} credits")
            else:
                printToScreen(f"   - {subcourse['type']} (Section ID: {subcourse['section_id']}) - "
                            f"Instructor: {subcourse['instructors']} - "
                            f"{subcourse['credits']} credits")
