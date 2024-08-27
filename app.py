from flask import Flask, render_template, request
import csv
import random

app = Flask(__name__)

def load_questions():
    questions = []
    with open('questions.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions

@app.route('/')
def index():
    questions = load_questions()
    selected_questions = random.sample(questions, 5)  # Select 10 random questions
    return render_template('quiz.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form
    questions = load_questions()
    score = 0

    for question in questions:
        q_text = question['Question Text']
        correct_answer = question['Correct Option']
        user_answer = user_answers.get(q_text)

        if user_answer == correct_answer:
            score += 1

    return f'You scored {score} out of 10!'

if __name__ == '__main__':
    app.run(debug=True)
