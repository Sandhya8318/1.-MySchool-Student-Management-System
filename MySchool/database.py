import mysql.connector
from mysql.connector import Error


# =========================================================
# MySchool Database Configuration
# =========================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "MySchool@123"
DB_NAME = "myschool"


# =========================================================
# CONNECT TO MYSQL SERVER
# =========================================================

def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if connection.is_connected():
            print("MySQL server connected successfully.")
            return connection

    except Error as e:
        print("MySQL connection error:", e)

    return None


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = connect_mysql()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
        )

        print(f"Database '{DB_NAME}' is ready.")

        cursor.close()
        connection.close()

        return True

    except Error as e:
        print("Database creation error:", e)

        try:
            connection.close()
        except:
            pass

        return False


# =========================================================
# GET DATABASE CONNECTION
# =========================================================

def get_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    connection = get_connection()

    if connection is None:
        print("Could not connect to MySchool database.")
        return False

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # ADMIN TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # -------------------------------------------------
        # REMOVE OLD STUDENTS TABLE
        #
        # This removes the old student_id / roll_no
        # structure causing the current errors.
        # -------------------------------------------------

        cursor.execute("DROP TABLE IF EXISTS students")

        # -------------------------------------------------
        # CREATE CORRECT STUDENTS TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                roll_no VARCHAR(50) NOT NULL UNIQUE,
                course VARCHAR(100) NOT NULL,
                branch VARCHAR(100) NOT NULL,
                semester VARCHAR(50),
                email VARCHAR(150),
                phone VARCHAR(20),
                address VARCHAR(255)
            )
        """)

        # -------------------------------------------------
        # DEFAULT ADMIN
        # -------------------------------------------------

        cursor.execute("""
            INSERT IGNORE INTO admins (username, password)
            VALUES ('admin', 'admin123')
        """)

        connection.commit()

        # -------------------------------------------------
        # SHOW TABLE STRUCTURE
        # -------------------------------------------------

        cursor.execute("DESCRIBE students")

        columns = cursor.fetchall()

        print("\nStudents table structure:")
        print("--------------------------------")

        for column in columns:
            print(
                column[0],
                "|",
                column[1],
                "|",
                "NULL=" + str(column[2]),
                "|",
                "KEY=" + str(column[3]),
                "|",
                "DEFAULT=" + str(column[4])
            )

        print("--------------------------------")

        cursor.close()
        connection.close()

        print("\nMySchool tables created successfully.")
        return True

    except Error as e:

        print("Table creation error:", e)

        try:
            connection.rollback()
            connection.close()
        except:
            pass

        return False


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    print("\n========================================")
    print("        MySchool Database Setup")
    print("========================================\n")

    if not create_database():
        print("\nDatabase creation failed.")
        return

    if not create_tables():
        print("\nTable creation failed.")
        return

    print("\n========================================")
    print("     MySchool Database Ready")
    print("========================================\n")


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":
    initialize_database()