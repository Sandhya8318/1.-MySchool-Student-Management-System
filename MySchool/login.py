import tkinter as tk
from tkinter import messagebox
from database import get_connection


class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("MySchool - Admin Login")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Background
        self.root.configure(bg="#f2f4f7")

        # Main Frame
        frame = tk.Frame(
            self.root,
            bg="white",
            padx=40,
            pady=35
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(
            frame,
            text="MySchool",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#1f4e79"
        ).pack(pady=(0, 5))

        tk.Label(
            frame,
            text="Student Management System",
            font=("Arial", 11),
            bg="white",
            fg="#666666"
        ).pack(pady=(0, 25))

        # Username
        tk.Label(
            frame,
            text="Username",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            frame,
            font=("Arial", 12),
            width=30
        )
        self.username_entry.pack(pady=(5, 15))

        # Password
        tk.Label(
            frame,
            text="Password",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            frame,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=(5, 20))

        # Login Button
        tk.Button(
            frame,
            text="LOGIN",
            font=("Arial", 11, "bold"),
            width=25,
            height=2,
            bg="#1f4e79",
            fg="white",
            cursor="hand2",
            command=self.login
        ).pack()

        tk.Label(
            frame,
            text="Default Login: admin / admin123",
            font=("Arial", 9),
            bg="white",
            fg="#888888"
        ).pack(pady=(15, 0))

        self.username_entry.focus()

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        connection = get_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Unable to connect to MySQL database."
            )
            return

        try:
            cursor = connection.cursor()

            query = """
                SELECT id, username
                FROM admins
                WHERE username = %s AND password = %s
            """

            cursor.execute(query, (username, password))

            admin = cursor.fetchone()

            cursor.close()
            connection.close()

            if admin:
                messagebox.showinfo(
                    "Login Successful",
                    "Welcome to MySchool!"
                )

                self.root.destroy()

                # Dashboard import
                from dashboard import Dashboard

                dashboard_root = tk.Tk()
                Dashboard(dashboard_root)
                dashboard_root.mainloop()

            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Something went wrong:\n{e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()