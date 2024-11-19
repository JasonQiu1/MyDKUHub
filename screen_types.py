from enum import Enum, auto

# All screens available in the app.
class ScreenType(Enum):
    LOGIN = auto(),
    HOME = auto(),
    CLASS_SEARCH = auto(),
    CLASS_RESULTS = auto(),
    USER_INFORMATION = auto(),
    ROSTER = auto(),
    ADVISEES = auto(),
    EXIT = auto(),
