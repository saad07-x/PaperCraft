import mysql.connector
import os
import shutil

# Define your MySQL credentials here
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root",
    "database": "mysql"
}

# Function to check if a paper exists in the database
def paper_exists(paper_name, cursor):
    cursor.execute('SELECT id FROM papers WHERE paper_name=%s', (paper_name,))
    return cursor.fetchone() is not None

# Function to create a new paper entry in the database
def create_paper_entry(paper_name, total_marks, cursor):
    cursor.execute('INSERT INTO papers (paper_name, total_marks) VALUES (%s, %s)', (paper_name, total_marks))

# Function to add a question to the database
def add_question_to_db(paper_id, difficulty, topic, marks, cursor):
    cursor.execute('INSERT INTO questions (paper_id, question_path, question_difficulty, topic_name, question_marks) VALUES (%s, %s, %s, %s, %s)',
                   (paper_id, 'path_to_question_folder', difficulty, topic, marks))

# Function to process a paper and its questions
def process_paper(paper_path, cursor):
    paper_name = os.path.basename(paper_path)
    
    # Check if the paper already exists in the database
    if not paper_exists(paper_name, cursor):
        total_marks = int(input(f"Enter total marks for {paper_name}: "))
        create_paper_entry(paper_name, total_marks, cursor)
    
    # Process questions in the 'Questions' folder
    questions_path = os.path.join(paper_path, 'Questions')
    for question_folder in os.listdir(questions_path):
        question_path = os.path.join(questions_path, question_folder)
        if os.path.isdir(question_path):
            difficulty = input(f"Enter difficulty for {question_folder}: ")
            topic = input(f"Enter topic for {question_folder}: ")
            marks = int(input(f"Enter marks for {question_folder}: "))
            
            # Get the paper_id for the current paper
            cursor.execute('SELECT id FROM papers WHERE paper_name=%s', (paper_name,))
            paper_id = cursor.fetchone()[0]
            
            # Add the question to the database
            add_question_to_db(paper_id, difficulty, topic, marks, cursor)

# Main function to process question papers in the 'data' folder
def process_question_papers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        data_folder = 'data'
        for paper_name in os.listdir(data_folder):
            print(paper_name)
            paper_path = os.path.join(data_folder, paper_name)
            print(paper_path)
            if os.path.isdir(paper_path):
                process_paper(paper_path, cursor)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error processing question papers: {e}")

if __name__ == "__main__":
    process_question_papers()
