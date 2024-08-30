from flask import Flask, render_template, request, redirect, url_for
import csv
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

def load_questions():
    questions = []
    with open('questions.csv', mode='r', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions

@app.route('/')
def index():
    questions = load_questions()
    selected_questions = random.sample(questions, 10)
    return render_template('quiz.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form
    username = user_answers.get('username')
    questions = load_questions()
    score = 0
    incorrect_questions = []

    for question in questions:
        q_text = question['Question Text']
        correct_answer = question['Correct Option']
        user_answer = user_answers.get(q_text)

        if user_answer == correct_answer:
            score += 1
        elif user_answer != None:
            incorrect_questions.append({
                'question_text': q_text,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'options': {
                    'A': question['Option A'],
                    'B': question['Option B'],
                    'C': question['Option C'],
                    'D': question['Option D'],
                }
            })

    # Send email with results
    send_email(username, score)

    return render_template('results.html', score=score, incorrect_questions=incorrect_questions, username=username)

def send_email(username, score):
    smtp_server = 'smtp.elasticemail.com'
    smtp_port = 2525  # or 465 for SSL
    smtp_username = 'frb3028@gmail.com'  # Your Elastic Email SMTP username
    smtp_password = '6B0F0C69510AE6FA47A196A67635CEDA74BF'  # Your Elastic Email SMTP password

    from_email = smtp_username  # Your Elastic Email account email
    to_email = smtp_username  # The recipient's email address
    
    subject = 'Quiz Results'
    body = f'User: {username}\nScore: {score}/10'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade to a secure connection
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
