from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

@app.route('/')
def hello():
    display =  """
            <h1>Site map:</h1>
            <br>
            <a href="http://127.0.0.1:5000/student">Student Completed course</a>
            <br>
            <a href="http://127.0.0.1:5000/instructor">Instructor student count</a>
            <br>
            <a href="http://127.0.0.1:5000/student_form">Find student details</a>
        """
    return display


@app.route('/instructor')
def instructor_template():
    database_path = "Test/810_startup.db"
    try:
        db = sqlite3.connect(database_path)
    except sqlite3.OperationalError:
        return (f"Error: Unable to open database at {database_path}")    
    else:
        query = """select i.CWID, i.Name, i.Dept, g.Course, count(*) as Stuents 
                        from instructors i left outer join grades g 
                        on g.InstructorCWID=i.CWID 
                        group by  i.CWID, i.Name, i.Dept, g.Course"""
        data = db.execute(query)
        instructor = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course,
                    'students': students} for cwid, name, dept, course, students in data]

        return render_template('instructor.html',
                            title="Stevens Repository",
                            page_header="Stevens instructor Repository",
                            table_title="Courses and student counts",
                            instructors=instructor)

@app.route('/student')
def student_template():
    database_path = "Test/810_startup.db"
    try:
        db = sqlite3.connect(database_path)
    except sqlite3.OperationalError:
        return (f"Error: Unable to open database at {database_path}")    
    else:
        query = """select s.CWID, s.Name, s.Major, count(g.Course) as completed
                    from students s join grades g
                    on s.CWID = g.StudentCWID
                    where g.Grade in ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')
                    group by s.CWID, s.Name, s.Major
                """
        data = db.execute(query)
        student = [{'cwid': cwid, 'name': name, 'major': major, 'completed': completed} for cwid, name, major, completed in data]

        return render_template('student.html',
                            title="Stevens Repository",
                            page_header="Stevens Student Repository",
                            table_title="Courses Copmeted by each student",
                            students=student)

@app.route('/student_form')
def choose_student():
    database_path = "Test/810_startup.db"
    try:
        db = sqlite3.connect(database_path)
    except sqlite3.OperationalError:
        return (f"Error: Unable to open database at {database_path}")    
    else:
        query= "SELECT CWID,NAME FROM students GROUP BY CWID,NAME"
        results = db.execute(query)
        data = [{'cwid':CWID,'name':NAME} for CWID, NAME in results]
        return render_template('student_form.html',title="Student Repository",student=data)

@app.route('/student_details' , methods=['POST'])
def student_form_template():
    database_path = "Test/810_startup.db"
    try:
        db = sqlite3.connect(database_path)
    except sqlite3.OperationalError:
        return (f"Error: Unable to open database at {database_path}")    
    else:
        if request.method == 'POST':
            cwid=request.form['cwid']
            print(cwid)
            query1 = "SELECT name FROM students WHERE CWID= ?"
            query2 = "SELECT course, grade FROM grades WHERE StudentCWID=? "
            args=(cwid,)
            db=sqlite3.connect(database_path)
            name = db.execute(query1,args)
            data = db.execute(query2,args)
            value = name.fetchone()
            table_title = (f"Grades Details for {value[0]}")
            grades=[{'course':course,'grade':grade} for course, grade in data]
            return render_template('student_details.html',title="Student Repository", table_title=table_title, details=grades)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')