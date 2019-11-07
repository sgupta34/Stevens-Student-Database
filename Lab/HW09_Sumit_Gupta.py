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

def file_reading_gen(path, sep='\t', head=False):
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
                self.grade_path = os.path.join(directory, 'grades.txt')
                self.major_path = os.path.join(directory, 'majors.txt')
                self.students = dict()
                self.instructors = dict()
                self.majors = dict()
                self.major_file()
                self.student_file()
                self.instructor_file()
                self.grades_file()
                self.major_table()
                self.student_table()
                self.instructor_table()
            except ValueError as err:
                print(err)
            except FileNotFoundError as err:
                print(err)
            except:
                print("Unexpected error encountered!")
        else:
            raise FileNotFoundError(f"No such Diectory as : {directory}")

    def major_file(self):
        """
        Add Major data into the dictionary from file
        """
        for info in file_reading_gen(self.major_path, '\t', True):
            major, flag, course = info
            if major not in self.majors:
                self.majors[major] = Major(info)
            self.majors[major].update_major(flag, course)

    def student_file(self):
        """
        Add Student data into the dictionary from file
        """
        for info in file_reading_gen(self.student_path, ';', True):
            cwid, name, major = info
            if major not in self.majors:
                raise ValueError(f'Major {major} not in system')
            if cwid not in self.students:
                self.students[cwid] = Student(info, self.majors[major])
            else:
                raise ValueError(f'Student name {name} with CWID \
                    {cwid} already present in the system.')

    def instructor_file(self):
        """
        Add instructor data into the dictionary from file
        """
        for info in file_reading_gen(self.instructor_path, '|', True):
            cwid, name, department = info
            if cwid not in self.instructors:
                self.instructors[cwid] = Instructor(info)
            else:
                raise ValueError(f'Instructor name {name} with CWID {cwid}\
                     of department {department} is already present in the system.')
    def grades_file(self):
        """
        Use grate.txt to add_course to Student and Instructor Classes
        """
        for info in file_reading_gen(self.grade_path, '|', True):
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
            courses = self.majors[student.major].update_courses(student.courses)
            cwid, name, major, _ = student.get_info()
            student_info = [cwid, name, major]
            for item in courses:
                student_info.append(item)
            pre_table.add_row(student_info)
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

    def major_table(self):
        """
        Use pretty table to print Major table
        """
        pre_table = PrettyTable(field_names=Major.ptm_header)
        for major in self.majors.values():
            pre_table.add_row(major.get_info())
        return pre_table

class Student:
    """
    Student Class to create student object
    """
    pts_header = ['CWID', 'Name', 'Major', 'Completed Courses',\
         'Remaining Required', 'Remaining Electives']
    def __init__(self, info, major_info):
        """
        Initialize student object with info parsed from text file
        """
        if len(info) != 3 or any(item.isspace() for item in info) or '' in info:
            raise ValueError("Student information incorrect in file.")
        self.cwid, self.name, self.major = info
        self.major_info = major_info
        self.courses = defaultdict(str)

    def add_course(self, course, grade):
        """
        Add the course using grade.txt
        """
        self.courses[course] = grade

    def get_info(self):
        """
        Return the list for pretty table
        """
        if not self.courses.items():
            return [self.cwid, self.name, []]
        return [self.cwid, self.name, self.major, sorted(list(self.courses.keys()))]
    def get_whole_info(self):
        """
        complete student information
        """
        return [self.cwid, self.name, self.major, self.courses] 

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
        Add the course using grade.txt
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

    def get_whole_info(self):
        """
        complete Instructor information
        """
        return [self.cwid, self.name, self.department, self.courses]
class Major:
    """
    Class to handle major
    """
    ptm_header = ['Major', 'Required Courses', 'Elective Courses']
    def __init__(self, info):
        """
        Initialize instructor object with info parsed from text file
        """
        if len(info) != 3 or any(item.isspace() for item in info) or '' in info:
            raise ValueError("Majors information incorrect in file.")
        self.major, self.flag, self.course = info
        if self.flag not in 'ER':
            raise ValueError("Value of flag can not be other than E or R. Check majors.txt file.")
        self.required = set()
        self.elective = set()

    def update_major(self, flag, course):
        """
        Update major info
        """
        if flag == 'R':
            self.required.add(course)
        if flag == 'E':
            self.elective.add(course)

    def get_info(self):
        """
        Return the major table data
        """
        return [self.major, sorted(list(self.required)), sorted(list(self.elective))]

    def update_courses(self, course):
        """
        Check if tudent pass or fail in the course taken
        """
        pass_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        completed = set()
        for sub, letter_grade in course.items():
            if letter_grade in pass_grade:
                completed.add(sub)
        left_req = self.left_required(completed)
        left_elec = self.left_electives(completed)
        return [sorted(list(completed)), left_req, left_elec]

    def left_required(self, course):
        """
        Find remaining Required courses for each student
        """
        if self.required.difference(course) == set():
            return None
        else:
            return self.required.difference(course)

    def left_electives(self, course):
        """
        Find the remaing electives for each student
        """
        if len(self.elective.difference(course)) < len(self.elective):
            return None
        else:
            return self.elective

    def get_whole_info(self):
        """
        complete student information
        """
        return [self.major, self.required, self.elective]

def main():
    """
    Main function to control the floq of code
    """
    dir_path = "Test"
    stevens = Repository(dir_path)
    print("Major Summary")
    print(stevens.major_table())
    print("Student Summary")
    print(stevens.student_table())
    print("Instructors Summary")
    print(stevens.instructor_table())
