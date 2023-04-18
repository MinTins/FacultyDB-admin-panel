from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Connect to the database
conn = pymysql.connect(
    host="db",
    user="root",
    password="qwerty123",
    database="facdb"
)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# View all students
@app.route('/students')
def students():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('students.html', students=students)

# Add a new student
@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        return redirect(url_for('students'))
    else:
        return render_template('add_student.html')

# Edit a student
@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id=%s", id)
    student = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute("UPDATE students SET name=%s, email=%s, phone=%s WHERE student_id=%s", (name, email, phone, id))
        conn.commit()
        return redirect(url_for('students'))
    else:
        return render_template('edit_student.html', student=student)

# Delete a student
@app.route('/students/delete/<int:id>')
def delete_student(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", id)
    conn.commit()
    return redirect(url_for('students'))

# Search for a student
@app.route('/students/search', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        students = cursor.fetchall()
        return render_template('students.html', students=students)
    else:
        return redirect(url_for('students'))

# View all courses
@app.route('/courses')
def courses():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template('courses.html', courses=courses)

# Add a new course
@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name) VALUES (%s)", course_name)
        conn.commit()
        return redirect(url_for('courses'))
    else:
        return render_template('add_course.html')

# Edit a course
@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE course_id=%s", id)
    course = cursor.fetchone()
    if request.method == 'POST':
        course_name = request.form['course_name']
        cursor.execute("UPDATE courses SET course_name=%s WHERE course_id=%s", (course_name, id))
        conn.commit()
        return redirect(url_for('courses'))
    else:
        return render_template('edit_course.html', course=course)

# Delete a course
@app.route('/courses/delete/<int:id>')
def delete_course(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE course_id=%s", id)
    conn.commit()
    return redirect(url_for('courses'))

# Search for a course
@app.route('/courses/search', methods=['GET', 'POST'])
def search_course():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE course_name LIKE %s", ('%' + search_query + '%'))
        courses = cursor.fetchall()
        return render_template('courses.html', courses=courses)
    else:
        return redirect(url_for('courses'))

# View all specialties
@app.route('/specialties')
def specialties():
    cursor = conn.cursor()
    cursor.execute("""SELECT s.specialty_id, s.specialty_name, f.faculty_name
        FROM specialties s
        JOIN faculties f ON s.faculty_id = f.faculty_id;""")
    specialties = cursor.fetchall()
    return render_template('specialties.html', specialties=specialties)

# Add a new specialty
@app.route('/specialties/add', methods=['GET', 'POST'])
def add_specialty():
    if request.method == 'POST':
        specialty_name = request.form['specialty_name']
        faculty_id = request.form['faculty_id']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO specialties (specialty_name, faculty_id) VALUES (%s, %s)", (specialty_name, faculty_id))
        conn.commit()
        return redirect(url_for('specialties'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculties")
        faculties = cursor.fetchall()
        return render_template('add_specialty.html', faculties=faculties)

# Edit a specialty
@app.route('/specialties/edit/<int:id>', methods=['GET', 'POST'])
def edit_specialty(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM specialties WHERE specialty_id=%s", id)
    specialty = cursor.fetchone()
    if request.method == 'POST':
        specialty_name = request.form['specialty_name']
        faculty_id = request.form['faculty_id']
        cursor.execute("UPDATE specialties SET specialty_name=%s, faculty_id=%s WHERE specialty_id=%s", (specialty_name, faculty_id, id))
        conn.commit()
        return redirect(url_for('specialties'))
    else:
        cursor.execute("SELECT * FROM faculties")
        faculties = cursor.fetchall()
        return render_template('edit_specialty.html', specialty=specialty, faculties=faculties)

# Delete a specialty
@app.route('/specialties/delete/<int:id>')
def delete_specialty(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM specialties WHERE specialty_id=%s", id)
    conn.commit()
    return redirect(url_for('specialties'))

# Search for a specialty
@app.route('/specialties/search', methods=['GET', 'POST'])
def search_specialty():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("""SELECT s.specialty_id, s.specialty_name, f.faculty_name
            FROM specialties s
            JOIN faculties f ON s.faculty_id = f.faculty_id WHERE s.specialty_name LIKE %s OR f.faculty_name LIKE %s""", ('%' + search_query + '%', '%' + search_query + '%'))
        specialties = cursor.fetchall()
        return render_template('specialties.html', specialties=specialties)
    else:
        return redirect(url_for('specialties'))

# View all groups
@app.route('/groups')
def groups():
    cursor = conn.cursor()
    cursor.execute("""SELECT gl.group_id, gl.group_name, c.course_name, s.specialty_name
        FROM groups_list gl
        JOIN courses c ON gl.course_id = c.course_id
        JOIN specialties s ON gl.specialty_id = s.specialty_id;""")
    groups = cursor.fetchall()
    return render_template('groups.html', groups=groups)

# Add a new group
@app.route('/groups/add', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        course_id = request.form['course_id']
        specialty_id = request.form['specialty_id']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO groups_list (group_name, course_id, specialty_id) VALUES (%s, %s, %s)", (group_name, course_id, specialty_id))
        conn.commit()
        return redirect(url_for('groups'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        cursor.execute("SELECT * FROM specialties")
        specialties = cursor.fetchall()
        return render_template('add_group.html', courses=courses, specialties=specialties)

# Edit a group
@app.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
def edit_group(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups_list WHERE group_id=%s", id)
    group = cursor.fetchone()
    if request.method == 'POST':
        group_name = request.form['group_name']
        course_id = request.form['course_id']
        specialty_id = request.form['specialty_id']
        cursor.execute("UPDATE groups_list SET group_name=%s, course_id=%s, specialty_id=%s WHERE group_id=%s", (group_name, course_id, specialty_id, id))
        conn.commit()
        return redirect(url_for('groups'))
    else:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        cursor.execute("SELECT * FROM specialties")
        specialties = cursor.fetchall()
        return render_template('edit_group.html', group=group, courses=courses, specialties=specialties)

# Delete a group
@app.route('/groups/delete/<int:id>')
def delete_group(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groups_list WHERE group_id=%s", id)
    conn.commit()
    return redirect(url_for('groups'))

# Search for a group
@app.route('/groups/search', methods=['GET', 'POST'])
def search_group():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("""SELECT gl.group_id, gl.group_name, c.course_name, s.specialty_name
            FROM groups_list gl
            JOIN courses c ON gl.course_id = c.course_id
            JOIN specialties s ON gl.specialty_id = s.specialty_id WHERE gl.group_name LIKE %s""", ('%' + search_query + '%'))
        groups = cursor.fetchall()
        return render_template('groups.html', groups=groups)
    else:
        return redirect(url_for('groups'))


# View all faculties
@app.route('/faculties')
def faculties():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculties")
    faculties = cursor.fetchall()
    return render_template('faculties.html', faculties=faculties)


# Add a new faculty
@app.route('/faculties/add', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faculties (faculty_name) VALUES (%s)", faculty_name)
        conn.commit()
        return redirect(url_for('faculties'))
    else:
        return render_template('add_faculty.html')


# Edit a faculty
@app.route('/faculties/edit/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculties WHERE faculty_id=%s", id)
    faculty = cursor.fetchone()
    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        cursor.execute("UPDATE faculties SET faculty_name=%s WHERE faculty_id=%s", (faculty_name, id))
        conn.commit()
        return redirect(url_for('faculties'))
    else:
        return render_template('edit_faculty.html', faculty=faculty)


# Delete a faculty
@app.route('/faculties/delete/<int:id>')
def delete_faculty(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faculties WHERE faculty_id=%s", id)
    conn.commit()
    return redirect(url_for('faculties'))


# Search for a faculty
@app.route('/faculties/search', methods=['GET', 'POST'])
def search_faculty():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculties WHERE faculty_name LIKE %s", ('%' + search_query + '%'))
        faculties = cursor.fetchall()
        return render_template('faculties.html', faculties=faculties)
    else:
        return redirect(url_for('faculties'))


# View all student groups
@app.route('/student_groups')
def student_groups():
    cursor = conn.cursor()
    cursor.execute("""SELECT sg.id, st.name, gl.group_name
        FROM student_group sg
        JOIN students st ON sg.student_id = st.student_id
        JOIN groups_list gl ON sg.group_id = gl.group_id;""")
    student_groups = cursor.fetchall()
    return render_template('student_groups.html', student_groups=student_groups)


# Add a new student group
@app.route('/student_groups/add', methods=['GET', 'POST'])
def add_student_group():
    if request.method == 'POST':
        student_id = request.form['student_id']
        group_id = request.form['group_id']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student_group (student_id, group_id) VALUES (%s, %s)", (student_id, group_id))
        conn.commit()
        return redirect(url_for('student_groups'))
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.execute("SELECT * FROM groups_list")
        groups = cursor.fetchall()
        return render_template('add_student_group.html', students=students, groups=groups)


# Edit a student group
@app.route('/student_groups/edit/<int:id>', methods=['GET', 'POST'])
def edit_student_group(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_group WHERE id=%s", id)
    student_group = cursor.fetchone()
    if request.method == 'POST':
        student_id = request.form['student_id']
        group_id = request.form['group_id']
        cursor.execute("UPDATE student_group SET student_id=%s, group_id=%s WHERE id=%s", (student_id, group_id, id))
        conn.commit()
        return redirect(url_for('student_groups'))
    else:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.execute("SELECT * FROM groups_list")
        groups = cursor.fetchall()
        return render_template('edit_student_group.html', student_group=student_group, students=students, groups=groups)


# Delete a student group
@app.route('/student_groups/delete/<int:id>')
def delete_student_group(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_group WHERE id=%s", id)
    conn.commit()
    return redirect(url_for('student_groups'))


# Search for a student group
@app.route('/student_groups/search', methods=['GET', 'POST'])
def search_student_group():
    if request.method == 'POST':
        search_query = request.form['search_query']
        cursor = conn.cursor()
        cursor.execute("""SELECT sg.id, st.name, gl.group_name
            FROM student_group sg
            JOIN students st ON sg.student_id = st.student_id
            JOIN groups_list gl ON sg.group_id = gl.group_id WHERE st.name LIKE %s OR gl.group_name LIKE %s""", ('%' + search_query + '%', '%' + search_query + '%'))
        student_groups = cursor.fetchall()
        return render_template('student_groups.html', student_groups=student_groups)
    else:
        return redirect(url_for('student_groups'))



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)