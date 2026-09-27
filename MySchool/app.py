from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from database import (
    get_connection,
    create_database,
    create_tables
)


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

app.secret_key = "myschool-secret-key-2026"


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

create_database()
create_tables()


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route("/")
def login():

    if "admin_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login_process():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    connection = get_connection()

    if connection is None:

        flash("Database connection failed.")

        return redirect(url_for("login"))

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM admins
        WHERE username = %s
        AND password = %s
        """,
        (username, password)
    )

    admin = cursor.fetchone()

    cursor.close()
    connection.close()

    if admin:

        session["admin_id"] = admin["id"]
        session["username"] = admin["username"]

        return redirect(url_for("dashboard"))

    flash("Invalid username or password.")

    return redirect(url_for("login"))


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()

    total_students = 0
    total_courses = 0
    total_branches = 0
    total_results = 0
    average_percentage = 0
    pass_students = 0
    fail_students = 0
    recent_results = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        # Total Students
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM students
        """)
        total_students = cursor.fetchone()["total"]


        # Total Courses
        cursor.execute("""
            SELECT COUNT(DISTINCT course) AS total
            FROM students
        """)
        total_courses = cursor.fetchone()["total"]


        # Total Branches
        cursor.execute("""
            SELECT COUNT(DISTINCT branch) AS total
            FROM students
        """)
        total_branches = cursor.fetchone()["total"]


        # Total Results
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM marks
        """)
        total_results = cursor.fetchone()["total"]


        # Average Percentage
        cursor.execute("""
            SELECT AVG((marks / max_marks) * 100) AS average_percentage
            FROM marks
            WHERE max_marks > 0
        """)

        result = cursor.fetchone()

        if result["average_percentage"] is not None:
            average_percentage = float(result["average_percentage"])


        # PASS Results
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM marks
            WHERE max_marks > 0
            AND ((marks / max_marks) * 100) >= 40
        """)

        pass_students = cursor.fetchone()["total"]


        # FAIL Results
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM marks
            WHERE max_marks > 0
            AND ((marks / max_marks) * 100) < 40
        """)

        fail_students = cursor.fetchone()["total"]


        # Recent Results
        cursor.execute("""
            SELECT
                students.name,
                students.roll_no,
                marks.subject,
                marks.marks,
                marks.max_marks,
                marks.exam_type
            FROM marks
            JOIN students
                ON marks.student_id = students.id
            ORDER BY marks.id DESC
            LIMIT 5
        """)

        recent_results = cursor.fetchall()


        cursor.close()
        connection.close()


    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_courses=total_courses,
        total_branches=total_branches,
        total_results=total_results,
        average_percentage=average_percentage,
        pass_students=pass_students,
        fail_students=fail_students,
        recent_results=recent_results
    )


# ==========================================
# STUDENT LIST
# ==========================================

@app.route("/students")
def students():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    connection = get_connection()

    student_list = []

    if connection:

        cursor = connection.cursor(dictionary=True)

        if search:

            query = """
                SELECT *
                FROM students
                WHERE
                    name LIKE %s
                    OR roll_no LIKE %s
                    OR course LIKE %s
                    OR branch LIKE %s
                    OR email LIKE %s
                ORDER BY id DESC
            """

            keyword = f"%{search}%"

            cursor.execute(
                query,
                (
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword
                )
            )

        else:

            cursor.execute(
                """
                SELECT *
                FROM students
                ORDER BY id DESC
                """
            )

        student_list = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template(
        "students.html",
        students=student_list,
        search=search
    )


# ==========================================
# ADD STUDENT PAGE
# ==========================================

@app.route("/students/add")
def add_student():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "add_student.html",
        student=None,
        page_title="Add Student"
    )


# ==========================================
# ADD STUDENT
# ==========================================

@app.route("/students/add", methods=["POST"])
def add_student_process():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()
    branch = request.form.get("branch", "").strip()
    semester = request.form.get("semester", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not roll_no or not course or not branch:

        flash(
            "Name, Roll Number, Course and Branch are required."
        )

        return redirect(url_for("add_student"))

    connection = get_connection()

    if connection is None:

        flash("Database connection failed.")

        return redirect(url_for("add_student"))

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students
            (
                name,
                roll_no,
                course,
                branch,
                semester,
                email,
                phone,
                address
            )
            VALUES
            (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                name,
                roll_no,
                course,
                branch,
                semester,
                email,
                phone,
                address
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Student added successfully.")

        return redirect(url_for("students"))

    except Exception as e:

        connection.rollback()
        connection.close()

        flash(f"Unable to add student: {e}")

        return redirect(url_for("add_student"))


# ==========================================
# EDIT STUDENT PAGE
# ==========================================

@app.route("/students/edit/<int:student_id>")
def edit_student(student_id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()

    student = None

    if connection:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

    if student is None:

        flash("Student not found.")

        return redirect(url_for("students"))

    return render_template(
        "add_student.html",
        student=student,
        page_title="Edit Student"
    )


# ==========================================
# UPDATE STUDENT
# ==========================================

@app.route(
    "/students/edit/<int:student_id>",
    methods=["POST"]
)
def update_student(student_id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()
    branch = request.form.get("branch", "").strip()
    semester = request.form.get("semester", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not roll_no or not course or not branch:

        flash(
            "Name, Roll Number, Course and Branch are required."
        )

        return redirect(
            url_for(
                "edit_student",
                student_id=student_id
            )
        )

    connection = get_connection()

    if connection is None:

        flash("Database connection failed.")

        return redirect(
            url_for(
                "edit_student",
                student_id=student_id
            )
        )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE students

            SET
                name = %s,
                roll_no = %s,
                course = %s,
                branch = %s,
                semester = %s,
                email = %s,
                phone = %s,
                address = %s

            WHERE id = %s
            """,
            (
                name,
                roll_no,
                course,
                branch,
                semester,
                email,
                phone,
                address,
                student_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Student updated successfully.")

        return redirect(url_for("students"))

    except Exception as e:

        connection.rollback()
        connection.close()

        flash(f"Unable to update student: {e}")

        return redirect(
            url_for(
                "edit_student",
                student_id=student_id
            )
        )


# ==========================================
# DELETE STUDENT
# ==========================================

@app.route(
    "/students/delete/<int:student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_connection()

    if connection is None:

        flash("Database connection failed.")

        return redirect(url_for("students"))

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Student deleted successfully.")

    except Exception as e:

        connection.rollback()
        connection.close()

        flash(f"Unable to delete student: {e}")

    return redirect(url_for("students"))

@app.route("/marks")
def marks():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            marks.id,
            students.name,
            students.roll_no,
            marks.subject,
            marks.marks,
            marks.max_marks,
            marks.exam_type
        FROM marks
        JOIN students ON marks.student_id = students.id
        ORDER BY marks.id DESC
    """)

    marks_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("marks.html", marks=marks_data)


@app.route("/marks/add", methods=["GET", "POST"])
def add_marks():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        student_id = request.form["student_id"]
        subject = request.form["subject"]
        marks_value = request.form["marks"]
        max_marks = request.form["max_marks"]
        exam_type = request.form["exam_type"]

        cursor.execute("""
            INSERT INTO marks
            (student_id, subject, marks, max_marks, exam_type)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            student_id,
            subject,
            marks_value,
            max_marks,
            exam_type
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Marks added successfully!", "success")
        return redirect(url_for("marks"))

    cursor.execute("""
        SELECT id, name, roll_no
        FROM students
        ORDER BY name
    """)

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("add_marks.html", students=students)


@app.route("/marks/delete/<int:mark_id>", methods=["POST"])
def delete_marks(mark_id):
    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM marks WHERE id = %s",
        (mark_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Marks deleted successfully!", "success")
    return redirect(url_for("marks"))
@app.route("/report-card")
def report_card():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, roll_no, course, branch, semester
        FROM students
        ORDER BY name
    """)

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "report_card_select.html",
        students=students
    )


@app.route("/report-card/<int:student_id>")
def student_report_card(student_id):
    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Student information
    cursor.execute("""
        SELECT id, name, roll_no, course, branch, semester, email, phone
        FROM students
        WHERE id = %s
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()

        flash("Student not found!", "error")
        return redirect(url_for("report_card"))

    # Student marks
    cursor.execute("""
        SELECT subject, marks, max_marks, exam_type
        FROM marks
        WHERE student_id = %s
        ORDER BY subject
    """, (student_id,))

    marks = cursor.fetchall()

    cursor.close()
    conn.close()

    total_marks = sum(item["marks"] for item in marks)
    total_max_marks = sum(item["max_marks"] for item in marks)

    if total_max_marks > 0:
        percentage = (total_marks / total_max_marks) * 100
    else:
        percentage = 0

    if marks:
        if percentage >= 40:
            overall_status = "PASS"
        else:
            overall_status = "FAIL"
    else:
        overall_status = "NO RESULT"

    return render_template(
        "report_card.html",
        student=student,
        marks=marks,
        total_marks=total_marks,
        total_max_marks=total_max_marks,
        percentage=percentage,
        overall_status=overall_status
    )
# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       MySchool Web Application")
    print("======================================")
    print("URL: http://127.0.0.1:5000")
    print("Username: admin")
    print("Password: admin123")
    print("======================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )