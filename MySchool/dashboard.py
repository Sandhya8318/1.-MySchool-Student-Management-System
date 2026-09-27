import mysql.connector
from mysql.connector import Error


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "MySchool@123"
DB_NAME = "myschool"


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        cursor.close()
        connection.close()

        print("Database ready.")

    except Error as e:

        print("Database creation error:", e)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        return connection

    except Error as e:

        print("Database connection error:", e)

        return None


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    connection = get_connection()

    if connection is None:
        return

    cursor = connection.cursor()

    # --------------------------------------
    # ADMIN TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    # --------------------------------------
    # STUDENTS TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            roll_no VARCHAR(50) UNIQUE NOT NULL,
            course VARCHAR(100) NOT NULL,
            branch VARCHAR(100) NOT NULL,
            semester VARCHAR(50),
            email VARCHAR(150),
            phone VARCHAR(20),
            address VARCHAR(255)
        )
    """)

    # --------------------------------------
    # DEFAULT ADMIN
    # --------------------------------------

    cursor.execute("""
        SELECT id
        FROM admins
        WHERE username = 'admin'
    """)

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO admins
            (username, password)
            VALUES
            ('admin', 'admin123')
        """)

    connection.commit()

    cursor.close()
    connection.close()

    print("Tables ready.")


# ==========================================
# RUN DATABASE SETUP
# ==========================================

if __name__ == "__main__":

    create_database()
    create_tables()

    print()
    print("====================================")
    print("     MySchool Database Ready")
    print("====================================")