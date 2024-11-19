# Main driver with application logic.

from screens import *

# Maps screen types to their classes
screenTypeToScreenClass = {
    ScreenType.LOGIN: LoginScreen,
    ScreenType.HOME: HomeScreen,
    #ScreenType.CLASS_SEARCH: ,
    #ScreenType.CLASS_RESULTS: ,
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

    def run(self):
        while True:
            self.screen.draw()
            if self.screenType == ScreenType.EXIT:
                return

            try:
                newScreenType, args = self.screen.prompt()
                if newScreenType:
                    self.screen = screenTypeToScreenClass[newScreenType](self, *args)
                    self.screenType = newScreenType
            except Exception as e:
                print("An error occurred:", e);

            self.drawScreenSpacer()

    def drawScreenSpacer(self):
        printToScreen("-----------------------")

def main():
    session = Session()
    session.run()
    return 0

main()
