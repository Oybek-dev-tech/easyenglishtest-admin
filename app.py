from flask import Flask, render_template, request, redirect, flash
import csv, os, requests

app = Flask(__name__)
app.secret_key = 'secret'

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID', '')

questions = []

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        flash('Faqat CSV fayl!')
        return redirect('/')
    content = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(content)
    for row in reader:
        questions.append(row)
    flash('CSV yuklandi!')
    return redirect('/')

@app.route('/send', methods=['GET'])
def send():
    for q in questions:
        payload = {
            'chat_id': CHAT_ID,
            'question': q['question'],
            'options': [q['option1'], q['option2'], q['option3'], q['option4']],
            'type': 'quiz',
            'correct_option_id': int(q['correct']) - 1,
            'explanation': q.get('explanation','')
        }
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPoll', json=payload)
    flash('Yuborildi!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
