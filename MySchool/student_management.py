import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import re


class StudentManagement:

    def __init__(self, root):
        self.root = root

        self.root.title("MySchool - Student Management")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        self.selected_student_id = None

        self.create_header()
        self.create_form()
        self.create_search()
        self.create_table()

        self.load_students()

    # =========================================================
    # HEADER
    # =========================================================
    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f4e78",
            height=70
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="Student Management",
            font=("Arial", 22, "bold"),
            bg="#1f4e78",
            fg="white"
        )
        title.pack(side="left", padx=25)

        back_btn = tk.Button(
            header,
            text="← Back to Dashboard",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#1f4e78",
            relief="flat",
            padx=15,
            pady=7,
            command=self.go_back
        )
        back_btn.pack(side="right", padx=25)

    # =========================================================
    # FORM
    # =========================================================
    def create_form(self):

        form_frame = tk.Frame(
            self.root,
            bg="white",
            bd=1,
            relief="solid"
        )
        form_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        title = tk.Label(
            form_frame,
            text="Student Information",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#222222"
        )
        title.grid(
            row=0,
            column=0,
            columnspan=6,
            sticky="w",
            padx=20,
            pady=(15, 10)
        )

        # ---------- Variables ----------
        self.name_var = tk.StringVar()
        self.roll_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.branch_var = tk.StringVar()
        self.semester_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()

        # ---------- Row 1 ----------
        self.create_label(form_frame, "Name", 1, 0)
        self.name_entry = self.create_entry(
            form_frame,
            self.name_var,
            1,
            1
        )

        self.create_label(form_frame, "Roll No", 1, 2)
        self.roll_entry = self.create_entry(
            form_frame,
            self.roll_var,
            1,
            3
        )

        self.create_label(form_frame, "Course", 1, 4)
        self.course_entry = self.create_entry(
            form_frame,
            self.course_var,
            1,
            5
        )

        # ---------- Row 2 ----------
        self.create_label(form_frame, "Branch", 2, 0)
        self.branch_entry = self.create_entry(
            form_frame,
            self.branch_var,
            2,
            1
        )

        self.create_label(form_frame, "Semester", 2, 2)
        self.semester_entry = self.create_entry(
            form_frame,
            self.semester_var,
            2,
            3
        )

        self.create_label(form_frame, "Email", 2, 4)
        self.email_entry = self.create_entry(
            form_frame,
            self.email_var,
            2,
            5
        )

        # ---------- Row 3 ----------
        self.create_label(form_frame, "Phone", 3, 0)
        self.phone_entry = self.create_entry(
            form_frame,
            self.phone_var,
            3,
            1
        )

        self.create_label(form_frame, "Address", 3, 2)
        self.address_entry = self.create_entry(
            form_frame,
            self.address_var,
            3,
            3
        )

        # ---------- Buttons ----------
        button_frame = tk.Frame(
            form_frame,
            bg="white"
        )
        button_frame.grid(
            row=4,
            column=0,
            columnspan=6,
            pady=15
        )

        add_btn = tk.Button(
            button_frame,
            text="➕ Add Student",
            font=("Arial", 10, "bold"),
            bg="#198754",
            fg="white",
            activebackground="#146c43",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.add_student
        )
        add_btn.pack(side="left", padx=5)

        update_btn = tk.Button(
            button_frame,
            text="✏ Update",
            font=("Arial", 10, "bold"),
            bg="#0d6efd",
            fg="white",
            activebackground="#0b5ed7",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.update_student
        )
        update_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete",
            font=("Arial", 10, "bold"),
            bg="#dc3545",
            fg="white",
            activebackground="#b02a37",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.delete_student
        )
        delete_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 10, "bold"),
            bg="#6c757d",
            fg="white",
            activebackground="#565e64",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.clear_fields
        )
        clear_btn.pack(side="left", padx=5)

        # Column configuration
        for column in [1, 3, 5]:
            form_frame.grid_columnconfigure(
                column,
                weight=1
            )

    # =========================================================
    # LABEL
    # =========================================================
    def create_label(self, parent, text, row, column):

        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#333333"
        )

        label.grid(
            row=row,
            column=column,
            sticky="w",
            padx=(20, 8),
            pady=6
        )

    # =========================================================
    # ENTRY
    # =========================================================
    def create_entry(self, parent, variable, row, column):

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        entry.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=8,
            pady=6,
            ipady=5
        )

        return entry

    # =========================================================
    # SEARCH
    # =========================================================
    def create_search(self):

        search_frame = tk.Frame(
            self.root,
            bg="#f4f6f9"
        )
        search_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        label = tk.Label(
            search_frame,
            text="Search Student:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f9",
            fg="#333333"
        )
        label.pack(side="left", padx=(0, 8))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=35,
            relief="solid",
            bd=1
        )
        search_entry.pack(
            side="left",
            ipady=6
        )

        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=("Arial", 10, "bold"),
            bg="#1f4e78",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.search_student
        )
        search_btn.pack(
            side="left",
            padx=8
        )

        show_all_btn = tk.Button(
            search_frame,
            text="Show All",
            font=("Arial", 10, "bold"),
            bg="#6c757d",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            command=self.load_students
        )
        show_all_btn.pack(side="left")

        search_entry.bind(
            "<Return>",
            lambda event: self.search_student()
        )

    # =========================================================
    # TABLE
    # =========================================================
    def create_table(self):

        table_frame = tk.Frame(
            self.root,
            bg="white"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        columns = (
            "id",
            "name",
            "roll_no",
            "course",
            "branch",
            "semester",
            "email",
            "phone",
            "address"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "id": "ID",
            "name": "Name",
            "roll_no": "Roll No",
            "course": "Course",
            "branch": "Branch",
            "semester": "Semester",
            "email": "Email",
            "phone": "Phone",
            "address": "Address"
        }

        widths = {
            "id": 50,
            "name": 150,
            "roll_no": 100,
            "course": 100,
            "branch": 100,
            "semester": 80,
            "email": 180,
            "phone": 120,
            "address": 200
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        # Vertical scrollbar
        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        # Horizontal scrollbar
        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.tree.pack(
            side="top",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_student
        )

    # =========================================================
    # VALIDATION
    # =========================================================
    def validate_form(self):

        name = self.name_var.get().strip()
        roll_no = self.roll_var.get().strip()
        course = self.course_var.get().strip()
        branch = self.branch_var.get().strip()
        semester = self.semester_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()

        # Required fields
        if not name:
            messagebox.showwarning(
                "Validation",
                "Please enter student name."
            )
            self.name_entry.focus()
            return False

        if not roll_no:
            messagebox.showwarning(
                "Validation",
                "Please enter roll number."
            )
            self.roll_entry.focus()
            return False

        if not course:
            messagebox.showwarning(
                "Validation",
                "Please enter course."
            )
            self.course_entry.focus()
            return False

        if not branch:
            messagebox.showwarning(
                "Validation",
                "Please enter branch."
            )
            self.branch_entry.focus()
            return False

        if not semester:
            messagebox.showwarning(
                "Validation",
                "Please enter semester."
            )
            self.semester_entry.focus()
            return False

        if not email:
            messagebox.showwarning(
                "Validation",
                "Please enter email."
            )
            self.email_entry.focus()
            return False

        if not phone:
            messagebox.showwarning(
                "Validation",
                "Please enter phone number."
            )
            self.phone_entry.focus()
            return False

        if not address:
            messagebox.showwarning(
                "Validation",
                "Please enter address."
            )
            self.address_entry.focus()
            return False

        # Name validation
        if not re.match(
            r"^[A-Za-z ]+$",
            name
        ):
            messagebox.showwarning(
                "Validation",
                "Name should contain only letters and spaces."
            )
            self.name_entry.focus()
            return False

        # Roll number validation
        if not re.match(
            r"^[A-Za-z0-9-]+$",
            roll_no
        ):
            messagebox.showwarning(
                "Validation",
                "Roll number can contain letters, numbers and '-'."
            )
            self.roll_entry.focus()
            return False

        # Semester validation
        if not semester.isdigit():

            messagebox.showwarning(
                "Validation",
                "Semester must be a number from 1 to 8."
            )

            self.semester_entry.focus()
            return False

        semester_number = int(semester)

        if semester_number < 1 or semester_number > 8:

            messagebox.showwarning(
                "Validation",
                "Semester must be between 1 and 8."
            )

            self.semester_entry.focus()
            return False

        # Email validation
        email_pattern = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}$"
        )

        if not re.match(
            email_pattern,
            email
        ):

            messagebox.showwarning(
                "Validation",
                "Please enter a valid email address."
            )

            self.email_entry.focus()
            return False

        # Phone validation
        if not phone.isdigit() or len(phone) != 10:

            messagebox.showwarning(
                "Validation",
                "Phone number must contain exactly 10 digits."
            )

            self.phone_entry.focus()
            return False

        return True

    # =========================================================
    # ADD STUDENT
    # =========================================================
    def add_student(self):

        if not self.validate_form():
            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO students
                (name, roll_no, course, branch, semester,
                 email, phone, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                self.name_var.get().strip(),
                self.roll_var.get().strip(),
                self.course_var.get().strip(),
                self.branch_var.get().strip(),
                self.semester_var.get().strip(),
                self.email_var.get().strip(),
                self.phone_var.get().strip(),
                self.address_var.get().strip()
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            self.clear_fields()
            self.load_students()

        except Exception as e:

            if "Duplicate entry" in str(e):

                messagebox.showerror(
                    "Duplicate Roll Number",
                    "This roll number already exists.\n"
                    "Please enter a different roll number."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Unable to add student.\n\n{e}"
                )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # LOAD STUDENTS
    # =========================================================
    def load_students(self):

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, name, roll_no, course, branch,
                       semester, email, phone, address
                FROM students
                ORDER BY id DESC
                """
            )

            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # SELECT STUDENT
    # =========================================================
    def select_student(self, event=None):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_student_id = values[0]

        self.name_var.set(values[1])
        self.roll_var.set(values[2])
        self.course_var.set(values[3])
        self.branch_var.set(values[4])
        self.semester_var.set(values[5])
        self.email_var.set(values[6])
        self.phone_var.set(values[7])
        self.address_var.set(values[8])

    # =========================================================
    # UPDATE STUDENT
    # =========================================================
    def update_student(self):

        if not self.selected_student_id:

            messagebox.showwarning(
                "Update",
                "Please select a student from the table first."
            )

            return

        if not self.validate_form():
            return

        result = messagebox.askyesno(
            "Confirm Update",
            "Are you sure you want to update this student?"
        )

        if not result:
            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                UPDATE students
                SET name=%s,
                    roll_no=%s,
                    course=%s,
                    branch=%s,
                    semester=%s,
                    email=%s,
                    phone=%s,
                    address=%s
                WHERE id=%s
            """

            values = (
                self.name_var.get().strip(),
                self.roll_var.get().strip(),
                self.course_var.get().strip(),
                self.branch_var.get().strip(),
                self.semester_var.get().strip(),
                self.email_var.get().strip(),
                self.phone_var.get().strip(),
                self.address_var.get().strip(),
                self.selected_student_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student updated successfully."
            )

            self.clear_fields()
            self.load_students()

        except Exception as e:

            if "Duplicate entry" in str(e):

                messagebox.showerror(
                    "Duplicate Roll Number",
                    "Another student already has this roll number."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Unable to update student.\n\n{e}"
                )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # DELETE STUDENT
    # =========================================================
    def delete_student(self):

        if not self.selected_student_id:

            messagebox.showwarning(
                "Delete",
                "Please select a student from the table first."
            )

            return

        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if not result:
            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE id=%s",
                (self.selected_student_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )

            self.clear_fields()
            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to delete student.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # SEARCH STUDENT
    # =========================================================
    def search_student(self):

        search_text = self.search_var.get().strip()

        if not search_text:

            self.load_students()
            return

        connection = None
        cursor = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            query = """
                SELECT id, name, roll_no, course, branch,
                       semester, email, phone, address
                FROM students
                WHERE name LIKE %s
                   OR roll_no LIKE %s
                   OR course LIKE %s
                   OR branch LIKE %s
                   OR email LIKE %s
                   OR phone LIKE %s
                ORDER BY id DESC
            """

            keyword = "%" + search_text + "%"

            cursor.execute(
                query,
                (
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword
                )
            )

            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=row
                )

            if not rows:

                messagebox.showinfo(
                    "Search",
                    "No student found."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search students.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # CLEAR FIELDS
    # =========================================================
    def clear_fields(self):

        self.selected_student_id = None

        self.name_var.set("")
        self.roll_var.set("")
        self.course_var.set("")
        self.branch_var.set("")
        self.semester_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")

        self.search_var.set("")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.name_entry.focus()

    # =========================================================
    # BACK TO DASHBOARD
    # =========================================================
    def go_back(self):

        result = messagebox.askyesno(
            "Back",
            "Return to Dashboard?"
        )

        if result:

            self.root.destroy()

            # Dashboard window was hidden using withdraw()
            # Find the main/root window and show it again.
            try:
                parent = self.root.master
                parent.deiconify()
                parent.lift()
            except Exception:
                pass