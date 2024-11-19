# Duke Kunshan University CS310 Introduction to Databases: Group Project

## Team members: Jason Qiu, Jingfeng Chen, Yinuo Guo

## Technologies: Python, MySQL

A course management system based on DKU's enrollment system where any user can view and search courses.

Course management is a very complex system that if done manually, can be both incredibly time-consuming and prone to error. This is due to the vast amount of information required to be stored, the high number of verification checks required for many actions, and the complexity of any advanced search of stored data.  

Students can enroll in courses and view the ones they are currently enrolled in, and instructors can view the courses they are teaching. It also provides a complex enrollment verification system considering the course’s prerequisites, anti-requisites, and time against the student’s information such as previous courses taken, currently enrolled course load, and registration holds. Instructors are able to set registration holds on students as well as see course rosters and the courses they are teaching.  

Using a student enrolling in a course as an example, you must check if the student has any registration holds. Then, you must check if adding this course will go over the student’s credit limit, which may be different for each student. Then, check if the student fulfills the prerequisites and does not violate any anti-requisites. Finally, check if adding the course will have any time conflicts with the courses that the student is already currently enrolled in.  

It follows then that creating a computer program and designing a database to manage all of this data and run these queries will significantly simplify the registrar’s workflow, improve registrar efficiency manifold, improve both student and instructor accessibility, and more.

# Running
```bash
python main.py
```

# Software Design

## Software Requirements Specification and Diagrams
View the SRS and database schema and use case diagrams in the `doc` folder.

## Creating new screens
The project interface is designed to be modular. To implement new screens, add a ScreenType for it in `screen_types.py`, inherit `Screen` and implement it in `screens.py`, and add a mapping from the screen type to class in `main.py`. All other screen classes and the application code like the `Session` class do not need to be modified. `Session` is closed to modification when extending the program with new screens. 

## Creating new views or user interfaces
`printToScreen` and `getUserInput` in `screen_base.py` can be modified to change the view of the application. Although it currently uses the terminal as the UI, it can be easily modified to print to an actual application window by changing those functions as well as `Session` without modifying any screens. This makes all the screens closed to modified when extending the program with new views.

# Contributing
First, read the documentation around `Session` in `main.py` and `Screen` in `screen_base.py`. 

When printing or getting user input, use the `printToScreen` and `getUserInput` utility functions to preserve abstraction between the model and view.
