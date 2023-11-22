# Examos - Question Paper Generator API

## Overview

Examos is a versatile question paper generator designed to create sets of questions for exams. These questions are stored in a structured JSON format and cover various subjects, topics, and difficulty levels.

## Question Store

### Structure

Each question in the question store is characterized by the following attributes:

- **question:** The actual question statement.
- **subject:** The subject to which the question belongs (e.g., OS, DBMS, DSA, OOPs).
- **topic:** The specific topic within the subject.
- **difficulty:** The difficulty level of the question (easy, medium, hard).
- **marks:** The marks assigned to the question based on difficulty.

### Subjects, Topics, Difficulty, and Marks

- **Subjects:** OS, DBMS, DSA, OOPs.
- **Topics:** Each subject has predefined topics.
- **Difficulty Levels:** Easy (2 marks), Medium (3 marks), Hard (5 marks).

##  Getting Started

1. Clone repository
```bash
git clone https://github.com/Dhruvin711/examos.git
```

2. Install requirements
```bash
cd examos/
pip install -r requirements.txt
```

3. Start server
```bash
python manage.py runserver
```

## Usage

### To add questions to Question-Store: /api/create-question/

To add more questions to the question store, make a POST request in the following format in JSON with one or more questions:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Discuss the role of the process control block in operating systems.",
      "subject": "OS",
      "topic": "Process Control Block",
      "difficulty": "easy",
      "marks": 2
    },
    // ... (more questions)
  ]
}
```

### To view Question-Store: /api/question-store/

To view all the questions that are store in Question-Store.

### To Generate Question Paper: /api/generate-question-paper/

To generate the question paper based on the total marks and the distribution of marks based on Difficulty, make a POST request in the following format in JSON.

```json
{
  "marks": 100,
  "easy": 20,
  "medium": 50,
  "hard": 30
}
```

```json
{
  "marks": 230,
  "easy": 30,
  "medium": 30,
  "hard": 40
}
```
