from enum import Enum, auto

# All screens available in the app.
class ScreenType(Enum):
    LOGIN = auto(),
    HOME = auto(),
    CLASS_SEARCH = auto(),
    CLASS_RESULTS = auto(),
    TEACHING_CLASSES = auto()
    USER_INFORMATION = auto(),
    ROSTER = auto(),
    ADVISEES = auto(),
    MANAGE_ENROLLMENT = auto(),
    PERSONAL_INFORMATION = auto(),
    MY_ACADEMIC_PROGRESS=auto,
    EXIT = auto()
