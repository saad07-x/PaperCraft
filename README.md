# PaperCraft

# Paper Generation System

This README provides instructions on how to use the Paper Generation System, which consists of two Python scripts: tag.py and main.py. This system allows you to generate new papers by selecting and tagging questions based on their marks, difficulty level, and topic.

## Setup SQL Credentials

Before using the system, make sure to set up your SQL database credentials in both tag.py and main.py. You should locate the following lines of code in both files and replace them with your actual database credentials:

```python
DB_CONFIG = {
'host': "your_db_host",
'user': "your_db_user",
'password': "your_db_password",
'database': "your_db_name"
}
```

## Storing Past Papers

All past papers should be stored in the data folder. You can add your past papers to this folder, ensuring that they are organized appropriately.

## Running tag.py

Open the tag.py script.

Run the script to tag questions based on their difficulty, topic, and marks. You will be prompted to provide input for each question:

Enter the difficulty level for quiz 1 (e.g., easy).
Enter the topic name for quiz 1 (e.g., algebra).
Enter the marks for quiz 1 (e.g., 10).
Repeat these steps for each question you want to tag. The script will process your input and tag the questions accordingly.

## Running main.py

Open the main.py script.

Run the script to generate a new paper. You will be prompted to provide the following input:

Enter a new paper name (e.g., test).
Enter the total marks for the paper (e.g., 20).
For each question in the paper:

Enter the difficulty level (e.g., easy).
Enter the topic name (e.g., algebra).
The script will generate a new paper based on your input, selecting questions that match the specified criteria. All requirements, including images, will be added to the paper.

The generated paper will be placed in a folder within the generated directory. You can find your newly generated paper there.

You've successfully used the Paper Generation System to tag and generate papers based on your specified criteria. Feel free to adjust the input parameters and configurations to suit your needs.
