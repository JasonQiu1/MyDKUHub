__package__ = "screens"

from screens.base import *
from screens.types import *
from screens.navigation import *

from screens.admin import *
from screens.misc import *

entryScreenType = ScreenType.LOGIN

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
