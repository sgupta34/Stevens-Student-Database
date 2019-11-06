# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 04:12:53 2019

@author: Sumit Gupta
@CWID : 10441745
"""
import os
from pathlib import Path
from collections import defaultdict
from prettytable import PrettyTable

def file_reading_gen(path,sep='\t',head=False):
    """
    Reading text files
    """
    try:
        file_pointer = open(path, 'r')
    except:
        raise FileNotFoundError(f"File not found: {path}")
    else:
        with file_pointer:
            for line in file_pointer:
                if head:
                    head = False
                    continue
                else:
                    yield tuple(line.strip().split(sep))
class Repository:
    """
    Repository of All the data for a university
    """
    def __init__(self, directory=os.getcwd()):
        """
        Initialize all the dictionary and print the pretty table
        """
        file_path = Path(directory)
        if file_path.exists():
            try:
                self.student_path = os.path.join(directory, 'students.txt')
                self.instructor_path = os.path.join(directory, 'instructors.txt')
                self.grade_path = os.path.join(directory, 'gradebad.txt')
                self.students = dict()
                self.instructors = dict()
                self.student_file()
                self.instructor_file()
                self.grades_file()
                self.student_table()
                self.instructor_table()
            except ValueError as e:
                print(e)
            except FileNotFoundError as e:
                print(e)
            except:
                print("Unexpected error encountered!")                
        else:
            raise FileNotFoundError(f"No such Diectory as : {directory}")

    def student_file(self):
        """
        Add Student data into the dictionary from file
        """
        for info in file_reading_gen(self.student_path):
            cwid, name, _ = info
            if cwid not in self.students:
                self.students[cwid] = Student(info)
            else:
                raise ValueError(f'Student name {name} with CWID {cwid} already present in the system.')

    def instructor_file(self):
        """
        Add instructor data into the dictionary from file
        """
        for info in file_reading_gen(self.instructor_path):
            cwid, name, department = info
            if cwid not in self.instructors:
                self.instructors[cwid] = Instructor(info)
            else:
                raise ValueError(f'Instructor name {name} with CWID {cwid} of department {department} is already present in the system.')
    def grades_file(self):
        """
        Use grate.txt to add_cource to Student and Instructor Classes
        """
        for info in file_reading_gen(self.grade_path):
            if len(info) != 4 or any(item.isspace() for item in info) or '' in info:
                raise ValueError("Grade file format is bad!!")
            cwid_student, course, letter_grade, cwid_instructor = info
            if cwid_student not in self.students.keys():
                raise ValueError(f'Student with CWID {cwid_student} is not in system.')
            if cwid_instructor not in self.instructors.keys():
                raise ValueError(f'Instructor with CWID {cwid_instructor} is not in system.')
            self.students[cwid_student].add_course(course, letter_grade)
            self.instructors[cwid_instructor].add_course(course)

    def student_table(self):
        """
        Use pretty table to print Student table
        """
        #print(self.students)
        pre_table = PrettyTable(field_names=Student.pts_header)
        for student in self.students.values():
            #cwid, name, courses = student.get_info()
            pre_table.add_row(student.get_info())
        return pre_table

    def instructor_table(self):
        """
        Use pretty table to print Instructor table
        """
        #print(self.instructors)
        pre_table = PrettyTable(field_names=Instructor.pti_header)
        for instructor in self.instructors.values():
            for row in instructor.get_info():
                pre_table.add_row(row)
        return pre_table

class Student:
    """
    Student Class to create student object
    """
    pts_header = ['CWID', 'Name', 'Courses']
    def __init__(self, info):
        """
        Initialize student object with info parsed from text file
        """
        if len(info) != 3 or any(item.isspace() for item in info) or '' in info:
            raise ValueError("Student information incorrect in file.")
        self.cwid, self.name, self.major = info
        self.courses = defaultdict(str)

    def add_course(self, course, grade):
        """
        Add the cource using grade.txt
        """
        self.courses[course] = grade

    def get_info(self):
        """
        Return the list for pretty table
        """
        if not self.courses.items():
            return [self.cwid, self.name, []]
        return [self.cwid, self.name, sorted(list(self.courses.keys()))]

class Instructor:
    """
    Instructor Class to create object
    """
    pti_header = ['CWID', 'Name', 'Dept', 'Courses', 'Students'] 
    def __init__(self, info):
        """
        Initialize instructor object with info parsed from text file
        """
        if len(info) != 3 or any(item.isspace() for item in info) or '' in info:
            raise ValueError("Instructor information incorrect in file.")
        self.cwid, self.name, self.department = info
        self.courses = defaultdict(int)

    def add_course(self, course):
        """
        Add the cource using grade.txt
        """
        self.courses[course] += 1

    def get_info(self):
        """
        Return the list for pretty table
        """
        if not self.courses.items():
            yield [self.cwid, self.name, self.department, None, 0]
        else:
            for subject, students in self.courses.items():
                yield [self.cwid, self.name, self.department, subject, students]

def main():
    """
    Main function to control the floq of code
    """
    dir_path = "Test"
    stevens = Repository(dir_path)
    print("Student Summary")
    print(stevens.student_table())
    print("Instructors Summary")
    print(stevens.instructor_table())
main()