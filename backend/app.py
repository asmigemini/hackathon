from flask import Flask, request, jsonify, render_template
import sqlite3
from ai.sentiment_analysis import analyze_sentiment
import random

app = Flask(__name__)
thoughts = [
"I am enough just as I am.",
"I choose to be happy today.",
"I am worthy of love and respect.",
"I embrace change and new beginnings.",
"My thoughts create my reality.",
"I am grateful for the beauty in my life.",
"I trust the process of life.",
"I radiate positivity and attract good energy.",
"I am in control of my own happiness.",
"Every day is a fresh start.",
"I choose to focus on the good.",
"I am capable of achieving my goals.",
"I am surrounded by love and support.",
"I forgive myself and release past mistakes.",
"I am resilient and can overcome challenges.",
"I celebrate my uniqueness and individuality.",
"I am open to receiving abundance.",
"I am deserving of all good things.",
"I choose love over fear.",
"I let go of what no longer serves me.",
"I trust my intuition to guide me.",
"I am constantly learning and growing.",
"I embrace my inner strength.",
"I am at peace with my past.",
"I choose to see the positive in every situation.",
"I am a magnet for success and prosperity.",
"I nurture my body and mind with love.",
"I am grateful for the present moment.",
"I am worthy of achieving my dreams.",
"I choose to be kind to myself.",
"I am capable of overcoming my fears.",
"I trust in my ability to create change.",
"I attract positive relationships into my life.",
"I am surrounded by opportunities for growth.",
"I am a source of inspiration to others.",
"I celebrate my achievements, big and small.",
"I am worthy of living a joyful life.",
"I am confident in my abilities.",
"I approach challenges with a positive mindset.",
"I am deserving of love and happiness.",
"I am learning to trust myself.",
"I find joy in the little things.",
"I am creating my own path in life.",
"I am capable of turning my dreams into reality.",
"I embrace my journey, no matter how winding.",
"I am enough, just as I am.",
"I choose to release negativity from my life.",
"I have the power to create positive change.",
"I am constantly evolving into a better version of myself.",
"I am open to new possibilities.",
"I celebrate my strengths and talents.",
"I am in tune with my feelings and emotions.",
"I trust that everything happens for a reason.",
"I am committed to my personal growth.",
"I choose to focus on what I can control.",
"I am resilient and can handle anything that comes my way.",
"I cultivate an attitude of gratitude.",
"I am worthy of my own love and respect.",
"I embrace the lessons life has to offer.",
"I am surrounded by abundance and joy.",
"I choose to see the beauty in every day.",
"I am open to the gifts life has to offer.",
"I attract positivity and good fortune.",
"I am deserving of happiness and fulfillment.",
"I trust my journey, even when I don’t understand it.",
"I am worthy of pursuing my passions.",
"I am capable of making my dreams come true.",
"I choose to fill my life with positivity.",
"I am in control of my thoughts and actions.",
"I find strength in vulnerability.",
"I am proud of my accomplishments.",
"I am capable of overcoming obstacles.",
"I choose to be my own best friend.",
"I am worthy of living my best life.",
"I am grateful for the love that surrounds me.",
"I am constantly attracting good fortune.",
"I trust in the timing of my life.",
"I am capable of handling whatever comes my way.",
"I choose to be present in each moment.",
"I am a unique individual with valuable contributions.",
"I embrace the challenges that help me grow.",
"I am worthy of creating the life I desire.",
"I choose to let go of fear and embrace love.",
"I am surrounded by positive energy.",
"I am deserving of a life filled with joy.",
"I trust my inner wisdom to guide me.",
"I am capable of achieving my highest potential.",
"I am grateful for the lessons life teaches me.",
"I am open to receiving love and compassion.",
"I choose to see the good in others.",
"I am creating a life that I love.",
"I am worthy of respect and kindness.",
"I am confident in my unique gifts and talents.",
"I embrace my imperfections as part of my journey.",
"I trust in my ability to navigate challenges.",
"I am surrounded by beauty and inspiration.",
"I choose to cultivate inner peace.",
"I am capable of creating positive habits.",
"I find joy in the present moment.",
"I am grateful for the abundance in my life.",
"I choose to prioritize my well-being.",
"I am worthy of forgiveness and self-compassion.",
"I am constantly evolving and growing.",
"I trust in the power of my dreams.",
"I am deserving of a fulfilling life.",
"I am capable of making a difference.",
"I choose to fill my mind with positive thoughts.",
"I am grateful for the opportunities that come my way.",
"I am a source of positivity in the world.",
"I embrace change as a part of life.",
"I am worthy of pursuing my passions.",
"I choose to be present and mindful.",
"I am surrounded by love and support.",
"I trust in my ability to create my reality.",
"I am deserving of success and happiness.",
"I am grateful for my journey.",
"I choose to focus on solutions rather than problems.",
"I am capable of achieving anything I set my mind to.",
"I embrace my uniqueness and individuality.",
"I trust that I am on the right path.",
"I am worthy of living my dreams.",
"I choose to be kind and compassionate.",
"I am surrounded by positive influences.",
"I find strength in my vulnerability.",
"I am grateful for the abundance that flows into my life.",
"I choose to embrace each day with gratitude.",
"I am capable of creating positive change.",
"I trust in the process of life.",
"I am deserving of love and acceptance.",
"I choose to let go of negativity.",
"I am a beacon of positivity and hope.",
"I am worthy of achieving my goals.",
"I embrace my strengths and talents.",
"I trust in my ability to overcome obstacles.",
"I am grateful for the love and support around me.",
"I choose to focus on the present moment.",
"I am capable of achieving greatness.",
"I am deserving of joy and happiness.",
"I trust my instincts and intuition.",
"I am grateful for my journey and growth.",
"I choose to surround myself with positivity.",
"I am capable of creating a life I love.",
"I embrace my inner power.",
"I am worthy of respect and love.",
"I trust in my ability to make the right choices.",
"I am surrounded by opportunities for success.",
"I choose to see the beauty in every day.",
"I am grateful for the lessons I have learned.",
"I am a source of inspiration to myself and others.",
"I am capable of achieving balance in my life.",
"I trust in my ability to create positive change.",
"I am deserving of a life filled with love and joy.",
"I choose to be gentle with myself.",
"I am grateful for my body and all it does for me.",
"I am capable of overcoming my fears.",
"I embrace my journey with an open heart.",
"I am worthy of living a fulfilling life.",
"I trust in my ability to navigate challenges.",
"I choose to focus on what truly matters.",
"I am surrounded by love and compassion.",
"I am deserving of happiness and peace.",
"I trust in my ability to learn and grow.",
"I am surrounded by beauty and inspiration.",
"I am worthy of living a life I love."]
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
                        mood_rating INTEGER CHECK (mood_rating IN (-1, 0, 1)) NOT NULL,
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

@app.route('/personalized', methods=['GET', 'POST'])
def personalized():
    if request.method == 'POST':
        data = request.get_json()
        mood = data['mood']
        
        sentiment, mood_rating = analyze_sentiment(mood)  

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO moods (mood, sentiment) VALUES (?, ?)
        ''', (mood, sentiment))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Mood logged successfully', 'mood_rating': mood_rating}), 200

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT mood, sentiment, timestamp FROM moods ORDER BY timestamp DESC LIMIT 5')
    moods = cursor.fetchall()
    conn.close()
    
    random_thought=random.choice(thoughts)

    mood_list = []
    for mood in moods:
        mood_label = mood[0]
        sentiment = mood[1]
        timestamp = mood[2]
        
        mood_list.append({
            'mood': mood_label,
            'sentiment': sentiment,
            'timestamp': timestamp
        })

    return render_template('personalized.html', mood_list=mood_list, random_thought=random_thought)

@app.route('/log_mood', methods=['POST'])
def log_mood():
    data = request.get_json()
    mood = data['mood']
    
    sentiment, mood_rating = analyze_sentiment(mood)  
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO moods (mood, sentiment) VALUES (?, ?)
    ''', (mood, sentiment))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Mood logged successfully', 'mood_rating': mood_rating}), 200

@app.route('/get_moods', methods=['GET'])
def get_moods():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT mood, sentiment, timestamp FROM moods')
    moods = cursor.fetchall()
    conn.close()

    mood_dict = {}
    for mood in moods:
        date = mood[2][:10] 
        sentiment = 1 if mood[1] == 'positive' else -1 if mood[1] == 'negative' else 0
        
        if date not in mood_dict:
            mood_dict[date] = []
        mood_dict[date].append(sentiment)

    mood_list = []
    for date, sentiments in mood_dict.items():
        average_sentiment = round(sum(sentiments) / len(sentiments))
        mood_label = 'positive' if average_sentiment == 1 else 'negative' if average_sentiment == -1 else 'neutral'
        mood_list.append({
            'mood': mood_label,
            'sentiment': mood_label,
            'timestamp': date
        })

    return jsonify(mood_list), 200

@app.route('/recommend_activities', methods=['GET'])
def recommend_activities():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT mood, sentiment FROM moods ORDER BY timestamp DESC LIMIT 1')
    latest_mood = cursor.fetchone()
    conn.close()

    activities = {
        'positive': ['Go for a walk', 'Watch a comedy movie', 'Read a book', 'Practice yoga', 'Do something good for someone else'],
        'neutral': ['Meditate for 10 minutes', 'Do some light stretching', 'Listen to music', 'Take a short nap'],
        'negative': ['Talk to a friend', 'Write in a journal', 'Engage in a creative hobby', 'Take deep breaths']
    }

    if latest_mood:
        sentiment = latest_mood[1]
        if sentiment == 'positive':
            recommended_activities = activities['positive']
        elif sentiment == 'neutral':
            recommended_activities = activities['neutral']
        else:
            recommended_activities = activities['negative']
        
        return render_template('activity_recommendation.html', activities=recommended_activities, mood=latest_mood[0]), 200
    
    return jsonify({'message': 'No mood data found'}), 404


@app.route('/mood-history')
def mood_history():
    conn = sqlite3.connect('data/mood.db')
    cursor = conn.cursor()
    cursor.execute("SELECT mood, sentiment, timestamp FROM moods")
    mood_list = cursor.fetchall()
    conn.close()
    
    return render_template('mood-history.html', mood_list=mood_list)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
