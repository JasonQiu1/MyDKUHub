# Main driver with application logic.

from os import getenv

from dotenv import load_dotenv

from db import *
from screens import ScreenType, screenTypeToScreenClass, entryScreenType

# Handles screen switching logic and is the main interface for the program.
class Session:
    def __init__(self, db_connection, debug=False):
        self.debug = debug
        self.db_connection = db_connection

        self.screenType = entryScreenType
        self.screen = screenTypeToScreenClass[self.screenType](self)
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
                    packed = self.screen.prompt()
                    args = ()
                    if packed:
                        newScreenType = packed[0]
                        if len(packed) > 1:
                            args = packed[1]

                    if self.debug:
                        print(f"Switching to screen: {newScreenType}, args: {args}")

                    if newScreenType:
                        self.screen = screenTypeToScreenClass[newScreenType](self, *args)
                        self.screenType = newScreenType
                except Exception as e:
                    print("An error occurred:", e)
                self.drawScreenSpacer()
        finally:
            if self.db_connection:
                self.db_connection.close()

    def drawScreenSpacer(self):
        print("-----------------------")


def main():
    load_dotenv()
    db_connection = DBConnection(getenv("DB_IP"), getenv("DB_USER"), getenv("DB_PASSWORD"), getenv("DB_NAME"))
    db_connection.connect()

    # TODO: Add error handling for if the DB connection failed

    # TODO: Add add prompt to init the DB if the connection succeeds but the DB does not exist

    session = Session(db_connection, debug=True if getenv("DEBUG") else False)
    session.run()
    return 0

main()
