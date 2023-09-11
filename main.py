import mysql.connector
import os
import shutil
import re

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
        

def create_folder_in_generated(name):
    generated_folder = 'generated'
    new_folder_path = os.path.join(generated_folder, name)

    try:
        os.mkdir(new_folder_path)
        print(f"Folder '{name}' created successfully inside 'generated'.")
        return new_folder_path  # Return the new folder path
    except FileExistsError:
        print(f"Folder '{name}' already exists inside 'generated'.")
        return new_folder_path  # Return the existing folder path
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None  # Return None in case of an error

        
def copy_folder(source_path, destination_path, question_number):
    try:
        shutil.copytree(source_path, destination_path)
        print(f"Folder copied from '{source_path}' to '{destination_path}' successfully.")

        # Rename .tex files to 'quiz.tex' inside the destination folder
        for root, _, files in os.walk(destination_path):
            for file in files:
                if file.endswith('.tex'):
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, 'quiz' + str(question_number + 1) + '.tex')
                    os.rename(old_path, new_path)
                    print(f"Renamed '{file}' to 'quiz.tex' inside '{destination_path}'.")
    except FileExistsError:
        print(f"Destination folder '{destination_path}' already exists. Copy operation aborted.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def copy_files_to_folder(source_folder, destination_folder):
    # Define the source path for the four files
    source_files = ['logo.JPG', 'logo.png', 'logo2.png', 'main.tex', 'packages.tex', 'title.tex', 'title2.tex']

    for file in source_files:
        source_file_path = os.path.join(source_folder, file)
        destination_file_path = os.path.join(destination_folder, file)

        try:
            shutil.copy2(source_file_path, destination_file_path)
            print(f"File '{file}' copied to '{destination_folder}' successfully.")
        except Exception as e:
            print(f"An error occurred while copying '{file}': {str(e)}")

def replace_quiz_number(tex_file_path, new_quiz_number):
    try:
        with open(tex_file_path, 'r') as file:
            content = file.read()

        # Use regular expression to find and replace the Quiz number
        pattern = r'(\\includegraphics\[.*\]{Questions/quiz )(\d+)(/images/.*?})'
        modified_content = re.sub(pattern, fr'\\includegraphics[{{scale=0.4}}]{{Questions/quiz {new_quiz_number}\3', content)

        # Save the modified content back to the file
        with open(tex_file_path, 'w') as file:
            file.write(modified_content)

        print(f"Modified Quiz number in '{tex_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
def update_main_tex(main_tex_path, tex_file_relative_path):
    tex_file_relative_path = tex_file_relative_path.replace("\\","/")
    try:
        with open(main_tex_path, 'r') as main_tex_file:
            content = main_tex_file.read()

        # Use regular expression to find the location where the new \include{} line should be added
        pattern = r'\\begin{questions}([\s\S]*?)\\end{questions}'
        match = re.search(pattern, content)

        if match:
            # Extract the content inside \begin{questions} and \end{questions}
            questions_content = match.group(1)

            # Generate the new \include{} line
            new_include_line = fr'\include{{{tex_file_relative_path}}}'
            
            # Append the new \include{} line to the questions_content
            updated_content = content.replace(match.group(0), f'\\begin{{questions}}{questions_content}{new_include_line}\n\\end{{questions}}')

            # Save the updated content back to the main.tex file
            with open(main_tex_path, 'w') as main_tex_file:
                main_tex_file.write(updated_content)

            print(f"Updated '{main_tex_path}' to include '{tex_file_relative_path}'.")
        else:
            print(f"Error: Unable to find the location to insert '{tex_file_relative_path}' in '{main_tex_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
                
if __name__ == "__main__":
    # Example usage:
    folder_name = 'test79'
    new_paper_folder = create_folder_in_generated(folder_name)
    copy_files_to_folder('Z:\Codes\PaperCraft\data\common', new_paper_folder)  # Replace with the actual source path

    num_questions = 3  # Set the number of questions you want to fetch

    for question in range(num_questions):
        question_difficulty = input("Enter question difficulty: ") # hard
        topic_name = input("Enter topic name: ") # algebra
        question_marks = int(input("Enter question marks: ")) # 10

        path = os.path.join('generated', folder_name)
        print(path)
        tex_file_relative_path = os.path.join('Questions', f'quiz {question + 1}', f'quiz {question + 1}.tex')

        try:
            setup_database()
            question_info = get_question_info(question_difficulty, topic_name, question_marks)
            
            if question_info:
                question_path, paper_name = question_info
                print(f"Question Path: {question_path}")
                print(f"New paper Path: {path}")
                copy_folder(question_path, os.path.join(path, 'Questions', 'quiz ' + str(question + 1)), question)
                # Example usage:
                tex_file_path =  path + '\Questions' + '\quiz ' + str(question + 1) + '\quiz' + str(question + 1) + '.tex' # Replace with the actual path to your .tex file
                print("hi")
                print (tex_file_path)
                new_quiz_number = str(question + 1)  # Replace with the new Quiz number
                replace_quiz_number(tex_file_path, new_quiz_number)
                # Update the main.tex file to include the new question
                main_tex_path = os.path.join(path, 'main.tex')
                update_main_tex(main_tex_path, tex_file_relative_path)

            else:
                print("No matching question found.")
        except Exception as e:
            print(f"An error occurred: {e}")
