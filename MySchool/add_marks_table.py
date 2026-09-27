from database import get_connection

def create_marks_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            subject VARCHAR(100) NOT NULL,
            marks INT NOT NULL,
            max_marks INT NOT NULL DEFAULT 100,
            exam_type VARCHAR(50) DEFAULT 'Final',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Marks table created successfully!")


if __name__ == "__main__":
    create_marks_table()