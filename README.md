# week-10
Homework 10

This week you'll continue to add new features to data repository you created last week. One of the most popular features is knowing what classes have been completed when signing up for classes for next semester.  However, users point out that it would be nice if your system also reported the remaining required courses.

Your assignment  this week has two components:

1. Create a GitHub repository to manage your growing software.    Start by creating a creating a GitHub repository and adding a  branch with your HW09 solution from last week to the repository.  Then create a new branch for this week's HW10 assignment.

2. Add the new feature to your solution to update the Student prettytable to show the remaining required and elective courses for each student.  This requires information about required courses and electives for each major.

Each major has a set of required courses that are required of all students.  Furthermore, a student must earn a grade of at least a 'C' for a course to count toward graduation.  (Valid grades include 'A', 'A-', 'B+', 'B', 'B-', 'C+', and 'C') Any student earning less than a 'C' must repeat the course until earning at least a 'C'.

Along with a set of required courses that every student must complete successfully, each major defines a set of electives and each student must successfully at least one of the electives associated with that major.  Students may take more than one elective, but they must take at least one of the electives associated with their major.

As frequently happens in real life, the format of the data files has changed since last week.  You'll need to download new copies of the data files from Canvas. Good thing you used your file_reading_gen() from HW08 which makes it trivial for you to read the new data files with their new formats and possible headers.   If you didn't use your file_reading_gen(), then you should refactor your code to make use of your file_reading_gen() function.

students.txt now has a header row that should be skipped and the separator has changed from '\t' to ';'.  Each row now looks like 'CWID;Name;Major'
instructors.txt now has a header row that should be skipped and the separator has changed from '\t' to '|'.  Each row now looks like 'CWID|Instructor|Dept'
grades.txt now has a header row that should be skipped and the separator has changed from '\t' to '|'.  Each row now looks like 'StudentCWID|Course|Grade|InstructorCWID'
majors.txt is a new data file with a header row that should be skipped and each field is separated by '\t'.  Each row has the format
major\tflag\tcourse

where the flag has the value 'R' if the course is a required course or 'E' if the course is an elective for that major.   You'll need to read the information about majors and use it to update your students summary table to add columns for "Remaining Required" and "Remaining electives" and then calculate the required courses that each student must take to graduate along with the remaining electives.  Note that students must take all of the required courses and at least one of the electives to graduate.

You should also include a new summary prettytable of majors including the name of the major, the required courses, and elective courses.

Here's the output of my implementation as a guideline.  Note that everything from HW09 is still present, I've just added the new Major summary prettytable and the Students prettytable adds fields for remaining required courses and remaining electives.

 HW10.png

To Do:

Create a GitHub repository for your Student Repository
Add a HW09 branch to your GitHub repository with the files from your HW09 solution
Create a new branch in your GitHub repository for this week's HW10 assignment.
Download the new students.txt,  instructors.txt, grades.txt, and majors.txt from Canvas
Update your HW09 code to use the new HW10 data files,
Add the new functionality to process majors and remaining classes,
Add a new Majors prettytable
Update the Student prettytable to include remaining classes and electives for each student
Implement automated tests to verify that the data in the prettytables matches the data from the input data files. 
 

You do NOT need to implement automated tests to catch all possible error conditions but your program should print relevant error messages when invalid or missing data is detected.
Your solution MAY print error messages and warnings to the user about inconsistent or bad data, e.g. a data file with the wrong number of fields or a grade for an unknown student or instructor.
Deliverables

The URL of your GitHub repository showing two branches: one for the HW09 code and this week's HW10 code.  Your repository should include all of the data files needed to run your solution
An updated Student summary table with the student's CWID, name, major, completed courses, remaining courses, and remaining electives
An instructor summary table (no changes from HW09)
A Major summary table with the name of the major, the required  courses, and the electives for that major 
Test your program and upload your program to Canvas when ready.   Be sure to handle unexpected cases, e.g. a student from the students.txt file who has no grades yet (she might be a first semester student), or student with a major that doesn't have a corresponding major in majors.txt.  You can be sure that your testing group (Prof JR) will have some curious test cases to try against your solution.
