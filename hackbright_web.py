"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def show_homepage():
    """Shows homepage"""

    students = hackbright.get_students()

    projects = hackbright.get_projects()

    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("students_search.html")


@app.route("/add-student")
def get_add_student_form():
    """Shows form for adding a student"""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student"""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("student_added.html", student=github)


@app.route("/project/<project_name>")
def display_project_info(project_name):
    """Shows info about a project"""

    # project = request.args.get('project')

    title, description, max_grade = hackbright.get_project_by_title(project_name)

    grades = hackbright.get_grades_by_title(project_name)

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           grade=max_grade,
                           grades=grades)


@app.route("/add-project")
def get_add_project_form():
    """Shows form for adding a project"""

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def project_add():
    """Add a project"""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_added.html", project=title)


@app.route("/add-grade")
def get_add_grade_form():
    """Shows form for adding a grade"""

    students = hackbright.get_students()

    projects = hackbright.get_projects()

    return render_template("grade_add.html",
                           students=students,
                           projects=projects)


@app.route("/grade-add", methods=['POST'])
def grade_add():
    """Add a grade"""

    student = request.form.get('student')
    project = request.form.get('project')
    grade = request.form.get('grade')

    if hackbright.get_grade_by_github_title(student, project):
        hackbright.update_grade(student, project, grade)
    else:
        hackbright.assign_grade(student, project, grade)

    return render_template("grade_added.html", student=student)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
