from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            assistant_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_type TEXT NOT NULL,
            duration INTEGER,
            completed BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Add root route for API status and documentation
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "available_endpoints": {
            "/": "GET - Show this documentation",
            "/chat": "POST - Send a message to the chatbot",
            "/exercise/log": "POST - Log an exercise session",
            "/history": "GET - Retrieve chat history"
        },
        "version": "1.0.0"
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    
    # Store chat in database
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_history (user_input, assistant_response)
        VALUES (?, ?)
    ''', (user_input, "Assistant response"))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

@app.route('/exercise/log', methods=['POST'])
def log_exercise():
    data = request.json
    exercise_type = data.get('type')
    duration = data.get('duration')
    
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO exercise_logs (exercise_type, duration, completed)
        VALUES (?, ?, ?)
    ''', (exercise_type, duration, True))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 50')
    history = c.fetchall()
    conn.close()
    
    return jsonify({"history": history})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)