__package__ = "screens"

from screens.base import *
from screens.types import *
from screens.navigation import *

from screens.student import *
from screens.instructor import *
from screens.admin import *
from screens.misc import *

entryScreenType = ScreenType.LOGIN

# Maps screen types to their classes
screenTypeToScreenClass = {
    # Navigation
    ScreenType.LOGIN: LoginScreen,
    ScreenType.HOME: HomeScreen,
    ScreenType.EXIT: ExitScreen,     

    # Available to all
    ScreenType.CLASS_SEARCH: ClassSearchScreen,
    ScreenType.CLASS_RESULTS: ClassResultsScreen,

    # Student
    ScreenType.PERSONAL_INFORMATION: PersonalInformationScreen,
    ScreenType.MY_ACADEMIC_PROGRESS: ShowMyProgressScreen,
    ScreenType.MANAGE_ENROLLMENT: ManageEnrollment,

    # Instructor
    ScreenType.TEACHING_CLASSES: ViewTeachingClassesScreen,
    ScreenType.ADVISEES: AdviseesScreen,
    ScreenType.INSTRUCTOR_INFORMATION: InstructorInformationScreen,
    
    # Admin
    ScreenType.ADMIN: AdminScreen,
    ScreenType.MANAGE_INSTRUCTOR: ManageInstructorScreen,
    ScreenType.MANAGE_DEPARTMENT: ManageDepartmentScreen,
    ScreenType.MANAGE_STUDENT: ManageStudentScreen,
    ScreenType.MANAGE_COURSE: ManageCourseScreen,
    ScreenType.STATISTICS: StatisticsScreen,
    ScreenType.STUDENT_STATS: StudentStatisticsScreen,
    ScreenType.INSTRUCTOR_STATS: InstructorStatisticsScreen,
    ScreenType.COURSE_STATS: CourseStatisticsScreen,
}
