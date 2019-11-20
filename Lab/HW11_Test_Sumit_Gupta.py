# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 04:12:53 2019

@author: Sumit Gupta
@CWID : 10441745
"""
import unittest
from HW11_Sumit_Gupta import file_reading_gen, Repository, main

class TestRepository(unittest.TestCase):
    """
    Class to test all the methods in HW09_Sumit_Gupta.py
    """
    def test_stevens_info(self):
        """
        Test if all the content of the file are loaded correctly or not
        """
        stevens = Repository('Test',False)
        students_info = {'10103': ['10103', 'Jobs, S', 'SFEN', {'SSW 810': 'A-', 'CS 501':'B'}],
                         '10115': ['10115', 'Bezos, J', 'SFEN', {'SSW 810': 'A', 'CS 546': 'F'}],
                         '10183': ['10183', 'Musk, E', 'SFEN', {'SSW 555': 'A', 'SSW 810': 'A'}],
                         '11714': ['11714', 'Gates, B', 'CS', {'SSW 810': 'B-', 'CS 546': 'A','CS 570': 'A-'}]
                         }
        instructors_info = {'98764': ['98764', 'Cohen, R', 'SFEN', {'CS 546': 1}],
                            '98763': ['98763', 'Rowland, J', 'SFEN', {'SSW 810': 4, 'SSW 555': 1}],
                            '98762': ['98762', 'Hawking, S', 'CS', {'CS 501': 1, 'CS 546': 1, 'CS 570': 1}]}
        majors_info = {'SFEN': ['SFEN', ('SSW 540', 'SSW 555', 'SSW 810'),('CS 501', 'CS 546')],
                       'CS': ['CS', ('SYS 800', 'SYS 612', 'SYS 671'),('SSW 565', 'SSW 810')]}
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
        stevens = Repository('Test',False)
        courses_info = {'10103': [['CS 501', 'SSW 810'], {'SSW 555', 'SSW 540'}, None],
                        '10115': [['SSW 810'], {'SSW 555', 'SSW 540'}, {'CS 501', 'CS 546'}],
                        '10183': [['SSW 555', 'SSW 810'], {'SSW 540'}, {'CS 501', 'CS 546'}],
                        '10175': [['SSW 567', 'SSW 564', 'SSW 687'], ['SSW 540', 'SSW 555'], \
                            ['CS 501', 'CS 513', 'CS 545']],
                        '11714': [['CS 546', 'CS 570', 'SSW 810'], None, None]}
        courses_dic = dict()
        for cwid, student in stevens.students.items():
            courses_dic[cwid] = stevens.majors[student.major].update_courses(student.courses)
        self.assertTrue(courses_dic, courses_info)
    def test_db(self):
        stevens = Repository('Test', False)
        instructor_db_info = [(98762, 'Hawking, S', 'CS', 'CS 501', 1), 
        (98762, 'Hawking, S', 'CS', 'CS 546', 1), (98762, 'Hawking, S', 'CS', 'CS 570', 1),
        (98763, 'Rowland, J', 'SFEN', 'SSW 555', 1), (98763, 'Rowland, J', 'SFEN', 'SSW 810', 4),
        (98764, 'Cohen, R', 'SFEN', 'CS 546', 1)]
        self.assertEqual(stevens.query_list, instructor_db_info)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    # To execute main function that prints the pretty table
    print("\n===============================================================================")
    main()
