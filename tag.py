import mysql.connector
import os
import shutil

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root",
    "database": "mysql"
}

def paper_exists(paper_name, cursor):
    cursor.execute('SELECT id FROM papers WHERE paper_name=%s', (paper_name,))
    return cursor.fetchone() is not None

def create_paper_entry(paper_name, total_marks, cursor):
    cursor.execute('INSERT INTO papers (paper_name, total_marks) VALUES (%s, %s)', (paper_name, total_marks))

def question_exists(question_path, cursor):
    cursor.execute('SELECT id FROM questions WHERE question_path=%s', (question_path,))
    return cursor.fetchone() is not None

def add_question_to_db(paper_id, difficulty, topic, marks, question_path, cursor):
    if not question_exists(question_path, cursor):
        cursor.execute('INSERT INTO questions (paper_id, question_path, question_difficulty, topic_name, question_marks) VALUES (%s, %s, %s, %s, %s)',
                       (paper_id, question_path, difficulty, topic, marks))
    else:
        print(f"Question with path '{question_path}' already exists. Skipping insertion.")

def process_paper(paper_path, cursor):
    paper_name = os.path.basename(paper_path)
    
    if not paper_exists(paper_name, cursor):
        total_marks = int(input(f"Enter total marks for {paper_name}: "))
        create_paper_entry(paper_name, total_marks, cursor)
    
    questions_path = os.path.join(paper_path, 'Questions')
    for question_folder in os.listdir(questions_path):
        question_path = os.path.join(questions_path, question_folder)
        if os.path.isdir(question_path):
            difficulty = input(f"Enter difficulty for {question_folder}: ")
            topic = input(f"Enter topic for {question_folder}: ")
            marks = int(input(f"Enter marks for {question_folder}: "))
            
            cursor.execute('SELECT id FROM papers WHERE paper_name=%s', (paper_name,))
            paper_id = cursor.fetchone()[0]
            
            add_question_to_db(paper_id, difficulty, topic, marks, question_path, cursor)

def process_question_papers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        data_folder = 'data'
        for paper_name in os.listdir(data_folder):
            paper_path = os.path.join(data_folder, paper_name)
            if os.path.isdir(paper_path):
                process_paper(paper_path, cursor)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error processing question papers: {e}")

if __name__ == "__main__":
    process_question_papers()
