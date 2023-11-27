# ------------------------------------------------------------------------------------------ #
# Title: Assignment07_ThomasPerkins
# Desc: This assignment demonstrates using classes, inheritance, and functions
# with structured error handling.
# Change Log: (Who, When, What)
#   TPerkins,11/25/2023,Created Script for Assignment 7
# ------------------------------------------------------------------------------------------ #

import json
import os
import io as _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str  # Hold the choice made by the user.
students: list = []  # a table of student data
file = _io.TextIOWrapper  # the default item type for this object.


class Person:
    """
    A class that defines a person object

    Parameters:
        :param: first_name: The first name of the person.
        :param: last_name: The last name of the person.

    ChaneLog:
        TPerkins, 11/25/2023, Created the class for Assignment 07.
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property  # (Use this decorator for the getter or accessor)
    def first_name(self):
        return self.__first_name.title()  # formatting code

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        return self.__last_name.title()  # formatting code

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        return f'{self.first_name},{self.last_name}'


class Student(Person):
    """
    A class that defines a student object, as a child of the Person class.

    Parameters:
        :param: course_name: The name of the course that the student is enrolling in.

    ChaneLog:
        TPerkins, 11/25/2023, Created the class for Assignment 07.
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name.title()  # formatting code

    @course_name.setter
    def course_name(self, value: str):
        if not value.isalpha() or value == "":  # is character or empty string
            self.__course_name = value
        else:
            raise ValueError("The course name should include a reference number.")

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    TPerkins, 11/23/2023, Created for Assignment06
    """

    # When the program starts, read the file data into a list of lists (table)
    # Extract the data from the file
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """
        This function reads a json file and creates a list of student data from the contents

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06
        :param file_name: Name of file to be read.
        :param student_data: List of student data.
        :return: list
        """
        global file
        try:
            if os.path.exists(file_name):
                file = open(file_name, "r")
            else:
                print("Existing file not found, creating new file.\n")
                file = open(file_name, "w")
                file.write("[]")
                file.close()
                file = open(file_name, "r")
            list_of_dictionary_data = json.load(file)  # the load function returns a list of dictionary rows.
            for student in list_of_dictionary_data:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)
            file.close()
        except Exception as e:
            IO.output_error_messages("There was an error opening the file!", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function writes the student data list to the json file.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06
        :param file_name: The file name to be written to
        :param student_data: The list of data to write
        :return: None
        """
        global file
        global num_records
        try:
            list_of_dictionary_data: list = []
            for student in student_data:
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name, "CourseName":
                        student.course_name}
                list_of_dictionary_data.append(student_json)
            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file, indent=4)
            file.close()
            print("The following data was saved to the file:")
            counter = 0
            for student in student_data:
                counter += 1
                if counter > num_records:
                    print(f'Student {student.first_name} '
                          f'{student.last_name} is enrolled in {student.course_name}')
            num_records = counter
        except Exception as e:
            if not file.closed:
                file.close()
            IO.output_error_messages("There was an error writing the data to the file. ", e)


class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    TPerkins, 11/23/2023, Created for Assignment06
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of choices to the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        print()
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice() -> str:
        """ This function gets a menu choice from the user.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing the exception object to avoid the technical message
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current list of student course data

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: None
        """
        # Process the data to create and display a custom message
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function records user input for student first name, last name,
        and course number.

        ChangeLog: (Who, When, What)
        TPerkins, 11/23/2023, Created for Assignment06

        :return: list
        """

        try:
            student = Student()
            student.first_name = input("Please enter the student's first name: ")
            if len(student.first_name) == 0:
                raise ValueError("The first name should not be blank.")
            student.last_name = input("Enter the student's last name: ")
            if len(student.last_name) == 0:
                raise ValueError("The last name should not be blank.")
            student.course_name = input("Please enter the name of the course: ")
            if len(student.course_name) == 0:
                raise ValueError("The course name should not be blank.")
            student_data.append(student)
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")

        except ValueError as e:
            IO.output_error_messages(ValueError.__doc__, e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data


# Open the data file
students = FileProcessor.read_data_from_file(FILE_NAME, students)
num_records = len(students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, 3, or 4.")

print("Program Ended")
