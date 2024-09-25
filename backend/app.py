from flask import Flask, request, jsonify, render_template
import sqlite3
from ai.sentiment_analysis import analyze_sentiment

app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect('data/mood.db')
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS moods (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        mood TEXT NOT NULL,
                        sentiment TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/selfcare')
def selfcare():
    return render_template('selfcare.html')

@app.route('/log_mood', methods=['POST'])
def log_mood():
    data = request.get_json()
    mood = data['mood']
    

    sentiment = analyze_sentiment(mood)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO moods (mood, sentiment) VALUES (?, ?)', (mood, sentiment))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Mood logged successfully'}), 200

@app.route('/get_moods', methods=['GET'])
def get_moods():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT mood, sentiment, timestamp FROM moods')
    moods = cursor.fetchall()
    conn.close()

    mood_list = []
    for mood in moods:
        mood_list.append({
            'mood': mood[0],
            'sentiment': mood[1],
            'timestamp': mood[2]
        })

    return jsonify(mood_list), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
