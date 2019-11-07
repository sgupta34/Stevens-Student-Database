# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 04:12:53 2019

@author: Sumit Gupta
@CWID : 10441745
"""
import unittest
from HW09_Sumit_Gupta import file_reading_gen, Repository, main

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
        self.assertEqual(file_check.major_path, 'Test\\majors.txt')
        with self.assertRaises(FileNotFoundError):
            file_check = Repository(".\\do_not_exist")
        with self.assertRaises(FileNotFoundError):
            for _ in file_reading_gen('Test\\do_not_exist.txt'):
                pass

    def test_stevens_info(self):
        """
        Test if all the content of the file are loaded correctly or not
        """
        stevens = Repository('Test')
        students_info = {'10103': ['10103', 'Baldwin, C', 'SFEN', {'SSW 567': 'A', 'SSW 564':\
             'A-', 'SSW 687': 'B', 'CS 501': 'B'}],
                         '10115': ['10115', 'Wyatt, X', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'B+'\
                             , 'SSW 687': 'A', 'CS 545': 'A'}],
                         '10172': ['10172', 'Forbes, I', 'SFEN', {'SSW 555': 'A', 'SSW 567': 'A-'}],
                         '10175': ['10175', 'Erickson, D', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'A',\
                              'SSW 687': 'B-'}],
                         '10183': ['10183', 'Chapman, O', 'SFEN', {'SSW 689': 'A'}],
                         '11399': ['11399', 'Cordova, I', 'SYEN', {'SSW 540': 'B'}],
                         '11461': ['11461', 'Wright, U', 'SYEN', {'SYS 800': 'A', 'SYS 750': 'A-',\
                              'SYS 611': 'A'}],
                         '11658': ['11658', 'Kelly, P', 'SYEN', {'SSW 540': 'F'}],
                         '11714': ['11714', 'Morton, A', 'SYEN', {'SYS 611': 'A', 'SYS 645': 'C'}],
                         '11788': ['11788', 'Fuller, E', 'SYEN', {'SSW 540': 'A'}]}
        instructors_info = {'98765': ['98765', 'Einstein, A', 'SFEN', {'SSW 567': 4, 'SSW 540': 3}],
                            '98764': ['98764', 'Feynman, R', 'SFEN', {'SSW 564': 3, 'SSW 687': 3, \
                                'CS 501': 1, 'CS 545': 1}],
                            '98763': ['98763', 'Newton, I', 'SFEN', {'SSW 555': 1, 'SSW 689': 1}],
                            '98762': ['98762', 'Hawking, S', 'SYEN', {}],
                            '98761': ['98761', 'Edison, A', 'SYEN', {}],
                            '98760': ['98760', 'Darwin, C', 'SYEN', {'SYS 800': 1, 'SYS 750': 1, \
                                'SYS 611': 2, 'SYS 645': 1}]}
        majors_info = {'SFEN': ['SFEN', ('SSW 555', 'SSW 564', 'SSW 567', 'SSW 540'), ('CS 513', \
            'CS 545', 'CS 501')],
                       'SYEN': ['SYEN', ('SYS 800', 'SYS 612', 'SYS 671'), ('SSW 565', 'SSW 810', \
                           'SSW 540')]}
        students_dic = dict()
        for cwid, student in stevens.students.items():
            students_dic[cwid] = student.get_whole_info()
        instructors_dic = dict()
        for cwid, instructor in stevens.instructors.items():
            instructors_dic[cwid] = instructor.get_whole_info()
        majors_dic = dict()
        for major, major_info in stevens.majors.items():
            majors_dic[major] = major_info.get_whole_info()
        self.assertEqual(students_dic, students_info)
        self.assertEqual(instructors_dic, instructors_info)
        for item, major in majors_dic.items():
            self.assertEqual(major[0], majors_info[item][0])
            self.assertTrue(major[1], majors_info[item][1])
            self.assertTrue(major[2], majors_info[item][2])
    def test_student_courses_info(self):
        """
        Test student successfully completed courses, remaining required courses and electives
        """
        stevens = Repository('Test')
        courses_info = {'10103': [['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'], ['SSW 540', \
            'SSW 555'], None],
                        '10115': [['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'], ['SSW 540', \
                            'SSW 555'], None],
                        '10172': [['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', \
                            'CS 513', 'CS 545']],
                        '10175': [['SSW 567', 'SSW 564', 'SSW 687'], ['SSW 540', 'SSW 555'], \
                            ['CS 501', 'CS 513', 'CS 545']],
                        '10183': [['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], \
                            ['CS 501', 'CS 513', 'CS 545']],
                        '11399': [['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None],
                        '11461': [['SYS 800', 'SYS 750', 'SYS 611'], ['SYS 612', 'SYS 671'], \
                            ['SSW 540', 'SSW 565', 'SSW 810']],
                        '11658': [[], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', \
                            'SSW 565', 'SSW 810']],
                        '11714': [['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], \
                            ['SSW 540', 'SSW 565', 'SSW 810']],
                        '11788': [['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None]}
        courses_dic = dict()
        for cwid, student in stevens.students.items():
            courses_dic[cwid] = stevens.majors[student.major].update_courses(student.courses)
        self.assertTrue(courses_dic, courses_info)
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    # To execute main function that prints the pretty table
    print("\n===============================================================================")
main()
