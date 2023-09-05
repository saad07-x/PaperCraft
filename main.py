import mysql.connector
import os
import shutil
import random

# Move database configuration to a separate file or use environment variables
DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "root",
    'database': "mysql"
}

def setup_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
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
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_question_info(difficulty, topic, marks):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT questions.question_path, papers.paper_name
                FROM questions
                INNER JOIN papers ON questions.paper_id = papers.id
                WHERE questions.question_difficulty = %s
                AND questions.topic_name = %s
                AND questions.question_marks = %s
            ''', (difficulty, topic, marks))

            result = cursor.fetchone()

        if result:
            question_path, paper_name = result
            return question_path, paper_name
        else:
            return None
    except Exception as e:
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    question_difficulty = "hard"
    topic_name = "algebra"
    question_marks = 10

    try:
        setup_database()
        question_info = get_question_info(question_difficulty, topic_name, question_marks)
        if question_info:
            question_path, paper_name = question_info
            print(f"Question Path: {question_path}")
            print(f"Paper Name: {paper_name}")
        else:
            print("No matching question found.")
    except Exception as e:
        print(f"An error occurred: {e}")
