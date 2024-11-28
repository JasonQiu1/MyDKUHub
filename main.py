# Main driver with application logic.

from screens import *

# Maps screen types to their classes
screenTypeToScreenClass = {
    ScreenType.LOGIN: LoginScreen,
    ScreenType.HOME: HomeScreen,
    ScreenType.CLASS_SEARCH: ClassSearchScreen,
    ScreenType.CLASS_RESULTS: ClassResultsScreen,
    ScreenType.MANAGE_ENROLLMENT: ManageEnrollment,
    ScreenType.PERSONAL_INFORMATION: PersonalInformationScreen,
    ScreenType.TEACHING_CLASSES: ViewTeachingClassesScreen,
    ScreenType.MY_ACADEMIC_PROGRESS: ShowMyProgressScreen,

    
    ScreenType.ADMIN: AdminScreen,
    ScreenType.MANAGE_INSTRUCTOR: ManageInstructorScreen,
    ScreenType.MANAGE_DEPARTMENT: ManageDepartmentScreen,
    ScreenType.MANAGE_STUDENT: ManageStudentScreen,
    ScreenType.MANAGE_COURSE: ManageCourseScreen,
    #ScreenType.USER_INFORMATION: ,
    #ScreenType.ROSTER: ,
    #ScreenType.ADVISEES: ,
    ScreenType.EXIT: ExitScreen,     
}

# Handles screen switching logic and is the main interface for the program.
class Session:
    def __init__(self):
        self.screenType = ScreenType.LOGIN
        self.screen = LoginScreen(self)
        self.user_level = None
        self.user_name = None
        self.user_netid = None

    def run(self):
        try:
            while True:
                self.screen.draw()
                if self.screenType == ScreenType.EXIT:
                    return

                try:
                    newScreenType, args = self.screen.prompt()
                    print(f"Switching to screen: {newScreenType}, args: {args}")
                    if newScreenType:
                        self.screen = screenTypeToScreenClass[newScreenType](self, *args)
                        self.screenType = newScreenType
                except Exception as e:
                    print("An error occurred:", e)
                self.drawScreenSpacer()
        finally:
            if Screen.db_connection:
                Screen.db_connection.close()

    def drawScreenSpacer(self):
        printToScreen("-----------------------")


def main():
    Screen.init_db("localhost", "root", "030108cjf", "PROJ1") # change this
    session = Session()
    session.run()
    return 0

main()
