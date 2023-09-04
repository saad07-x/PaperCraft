import mysql.connector
import os
import shutil

def setup_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="mysql"
        )

        cursor = conn.cursor()

        # Task 2: Create Tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                paper_name VARCHAR(255),
                total_marks INT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                paper_id INT,
                question_path TEXT,
                question_difficulty VARCHAR(255),
                topic_name VARCHAR(255),
                question_marks INT
            )
        ''')

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error setting up the database: {e}")
        



# setup_database()