import os
import re

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

# Example usage:
tex_file_path = r'generated\test6\Questions\Quiz 2\quiz2.tex'  # Replace with the actual path to your .tex file
new_quiz_number = '5'  # Replace with the new Quiz number

replace_quiz_number(tex_file_path, new_quiz_number)
