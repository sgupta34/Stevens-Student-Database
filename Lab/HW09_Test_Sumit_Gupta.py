# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 04:12:53 2019

@author: Sumit Gupta
@CWID : 10441745
"""
import unittest
from HW09_Sumit_Gupta import file_reading_gen, Repository, \
    Student, Instructor, main

class TestRepository(unittest.TestCase):
    """
    Class to test all the methods in HW09_Sumit_Gupta.py
    """
    def test_directory(self):
        """
        Test if directory/files exist or not
        """
        file_check = Repository("Test")
        self.assertEqual(file_check.student_path, 'Test\\students.txt')
        self.assertEqual(file_check.instructor_path, 'Test\\instructors.txt')
        self.assertEqual(file_check.grade_path, 'Test\\grades.txt')
        with self.assertRaises(FileNotFoundError):
            file_check = Repository(".\\do_not_exist")
        with self.assertRaises(FileNotFoundError):
            for _ in file_reading_gen('Test\\do_not_exist.txt'):
                pass

    def test_all_instructor(self):
        """
        test if all the instructors from file are read or not
        """
        repo = Repository("Test")
        instructor_list = {'98765', '98764', '98763', '98762', '98761', '98760'}
        check_list = {cwid for cwid in repo.instructors}
        self.assertEqual(instructor_list, check_list)

    def test_all_student(self):
        """
        test if all the students from file are read or not
        """
        repo = Repository("Test")
        student_list = {'10103', '11123', '11798', '10115', '10172', '10175', \
            '10183', '11399', '11461', '11658', '11714', '11788'}
        check_list = {cwid for cwid in repo.students}
        self.assertEqual(student_list, check_list)

    def test_student_file(self):
        """
        Check for value error that are raised in student object creation
        """
        tup = ('13111', 'Sumit') #hard coded method
        with self.assertRaises(ValueError):
            _ = Student(tup)
        repo1 = Repository("Test")
        # Test for Duplicates
        repo1.student_path = ".\\Test\\studentbad.txt"
        with self.assertRaises(ValueError):
            repo1.student_file()

    def test_instructor_file(self):
        """
        Check for value error that are raised in instructor object creation
        """
        tup = ('13111', 'Sumit', 'CSE', 'Extra') #hard coded method
        with self.assertRaises(ValueError):
            _ = Instructor(tup)
        repo = Repository("Test")
        # Test for duplicates
        repo.instructor_path = ".\\Test\\instructorbad.txt"
        with self.assertRaises(ValueError):
            repo.instructor_file()

    def test_grade_file(self):
        """
        Check for value error that are raised in grades_file()
        """
        repo = Repository("Test")
        # Test for less fields in the file.
        # Test for Missing Student from the system
        # Test for Missing instructor from the system
        repo.grade_path = ".\\Test\\gradebad.txt"
        with self.assertRaises(ValueError):
            repo.grades_file()

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    # To execute main function that prints the pretty table
    print("\n===============================================================================")
    main()
