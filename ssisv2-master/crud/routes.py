from flask import render_template, url_for, request, redirect, flash
from crud.forms import CourseSearchForm, SearchForm, StudentForm, CourseForm, CollegeSearchForm, CollegeForm, CollegeSearchForm
from crud import application, my_sql
from cloudinary.uploader import upload, destroy


@application.route("/students", methods=["POST", "GET"])
@application.route("/", methods=["POST", "GET"])
def students():
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    form = SearchForm()

    return render_template("students.html", title="Students", 
                            students=students, form=form)

@application.route("/add_student", methods=["POST", "GET"])
def add_a_student():
    connection = my_sql.connect()
    cursor = connection.cursor()

    form = StudentForm()
    cursor.execute("SELECT course_code FROM Course")
    courses = cursor.fetchall()
    form.course.choices = [course[0] for course in courses]

    if request.method == "POST" and form.validate_on_submit():
        id_number = form.id_number.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        course = form.course.data
        year_level = form.year_level.data
        gender = form.gender.data
        profile_pic = form.profile_pic.data

        profile_pic = upload(profile_pic.read()).get('url')


        cursor.execute("INSERT INTO Student VALUES (%s, %s, %s, %s, %s, %s,%s)",
                       (id_number, first_name, last_name, course, year_level, gender,profile_pic))
        connection.commit()

        flash("Student {} has been added successfully.".format(form.id_number.data), 
              "success")
        return redirect(url_for("students"))

    return render_template("add_student.html", title="Add a Student", 
                            legend="Add a Student", form=form)

@application.route("/update/<id_number>", methods=["POST", "GET"])
def update(id_number):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Student WHERE id_number = %s", 
                    (id_number))
    student = cursor.fetchall()

    form = StudentForm()
    cursor.execute("SELECT course_code FROM Course")
    courses = cursor.fetchall()
    form.course.choices = [course[0] for course in courses]

    if form.validate_on_submit():
        id_number = form.id_number.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        course = form.course.data
        year_level = form.year_level.data
        gender = form.gender.data
        profile_pic= form.profile_pic.data

        profile_pic = upload(profile_pic.read()).get('url')

        cursor.execute("""
            UPDATE Student
            SET id_number = %s,
                first_name = %s,
                last_name = %s,
                course = %s,
                year_level = %s,
                gender = %s,
                profile_pic=%s
                WHERE id_number = %s
            """, (id_number, first_name, last_name, course, year_level, gender,profile_pic,id_number)
        )
        cursor.close()
        connection.commit()

        flash("Student {}'s records have been updated successfully.".format(id_number),
              "success")
        return redirect((url_for("students")))

    elif request.method == "GET":
        form.id_number.data = student[0][0]
        form.first_name.data = student[0][1]
        form.last_name.data = student[0][2]
        form.course.data = student[0][3]
        form.year_level.data = student[0][4]
        form.gender.data = student[0][5]
        form.profile_pic.data = student[0][6]
        form.add.label.text = "Update"

    return render_template("add_student.html", title="Update Student Records",
                            legend="Update Student Records", form=form)

@application.route("/delete/<id_number>", methods=["POST", "GET"])
def delete(id_number):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Student WHERE id_number = %s", (id_number,))
    cursor.close()

    connection.commit()
    connection.close()

    destroy(public_id="ssims-flask/{}".format(id_number))

    flash("Student {}'s records have been deleted successfully.".format(id_number),
          "danger")
    return redirect((url_for("students")))

@application.route("/search", methods=["POST", "GET"])
def search():
    form = SearchForm()

    pairs = {
        "ID Number": "id_number",
        "First name": "first_name",
        "Last name": "last_name",
        "Course": "course",
        "Year Level": "year_level",
        "Gender": "gender"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Student WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", title="Students", 
                            students=students, form=form)

@application.route("/courses")
def courses():
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    cursor.close()
    connection.close()

    form = CourseSearchForm()

    return render_template("courses.html", title="Courses", 
                            courses=courses, form=form)

@application.route("/add_course", methods=["POST", "GET"])
def add_a_course():
    connection = my_sql.connect()
    cursor = connection.cursor()

    form = CourseForm()
    cursor.execute("SELECT college_code FROM College")
    colleges = cursor.fetchall()
    form.college.choices = [college[0] for college in colleges]

    if request.method == "POST" and form.validate_on_submit():
        course_code = form.course_code.data
        course_name = form.course_name.data
        college = form.college.data

        cursor.execute("INSERT INTO Course VALUES (%s, %s, %s)",
                       (course_code, course_name, college))
        connection.commit()

        flash("Course {} has been added successfully.".format(form.course_code.data), 
              "success")
        return redirect(url_for("courses"))

    return render_template("add_course.html", title="Add a Course", 
                            legend="Add a Course", form=form)

@application.route("/update_a_course/<course_code>", methods=["POST", "GET"])
def update_a_course(course_code):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Course WHERE course_code = %s", 
                    (course_code))
    course = cursor.fetchall()

    form = CourseForm()
    cursor.execute("SELECT college_code FROM College")
    colleges = cursor.fetchall()
    form.college.choices = [college[0] for college in colleges]

    if form.validate_on_submit():
        course_code = form.course_code.data
        course_name = form.course_name.data
        college = form.college.data

        cursor.execute("""
            UPDATE Course 
            SET course_code = %s,
                course_name = %s,
                college = %s
                WHERE course_code = %s
            """, (course_code, course_name, college, course_code)
        )
        cursor.close()
        connection.commit()

        flash("Course {}'s records have been updated successfully.".format(course_code), 
              "success")
        return redirect((url_for("courses")))

    elif request.method == "GET":
        form.course_code.data = course[0][0]
        form.course_name.data = course[0][1]
        form.college.data = course[0][2]
        form.add.label.text = "Update"

    return render_template("add_course.html", title="Update Course Records", 
                            legend="Update Course Records", form=form)

@application.route("/delete_a_course/<course_code>", methods=["POST", "GET"])
def delete_a_course(course_code):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Course WHERE course_code = %s", (course_code,))
    cursor.close()

    connection.commit()
    connection.close()

    flash("Course {} has been deleted successfully.".format(course_code), 
          "danger")
    return redirect((url_for("courses")))

@application.route("/course_search", methods=["POST", "GET"])
def course_search():
    form = CourseSearchForm()

    pairs = {
        "Course code": "course_code",
        "Course name": "course_name",
        "College": "college"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Course WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("courses.html", title="Courses", 
                            courses=courses, form=form)

@application.route("/colleges")
def colleges():
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM College")
    colleges = cursor.fetchall()
    cursor.close()
    connection.close()

    form = CollegeSearchForm()

    return render_template("colleges.html", title="Colleges", 
                            colleges=colleges, form=form)

@application.route("/add_college", methods=["POST", "GET"])
def add_a_college():
    connection = my_sql.connect()
    cursor = connection.cursor()

    form = CollegeForm()

    if request.method == "POST" and form.validate_on_submit():
        college_code = form.college_code.data
        college_name = form.college_name.data

        cursor.execute("INSERT INTO College VALUES (%s, %s)",
                       (college_code, college_name))
        connection.commit()

        flash("College {} has been added successfully.".format(form.college_code.data), 
              "success")
        return redirect(url_for("colleges"))

    return render_template("add_college.html", title="Add a College", 
                            legend="Add a College", form=form)

@application.route("/update_a_college/<college_code>", methods=["POST", "GET"])
def update_a_college(college_code):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM College WHERE college_code = %s", 
                    (college_code))
    college = cursor.fetchall()

    form = CollegeForm()

    if form.validate_on_submit():
        college_code = form.college_code.data
        college_name = form.college_name.data

        cursor.execute("""
            UPDATE College 
            SET college_code = %s,
                college_name = %s 
                WHERE college_code = %s
            """, (college_code, college_name, college_code)
        )
        cursor.close()
        connection.commit()

        flash("College {}'s records have been updated successfully.".format(college_code), 
              "success")
        return redirect((url_for("colleges")))

    elif request.method == "GET":
        form.college_code.data = college[0][0]
        form.college_name.data = college[0][1]
        form.add.label.text = "Update"

    return render_template("add_college.html", title="Update College Records", 
                            legend="Update College Records", form=form)

@application.route("/delete_a_college/<college_code>", methods=["POST", "GET"])
def delete_a_college(college_code):
    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM College WHERE college_code = %s", (college_code,))
    cursor.close()

    connection.commit()
    connection.close()

    flash("College {} has been deleted successfully.".format(college_code), 
          "danger")
    return redirect((url_for("colleges")))

@application.route("/college_search", methods=["POST", "GET"])
def college_search():
    form = CollegeSearchForm()

    pairs = {
        "College code": "college_code",
        "College name": "college_name"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM College WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    colleges = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("colleges.html", title="Colleges", 
                            colleges=colleges, form=form)