"""
This is going to be the Kahoot Server file! 
Below is the simple server implementation
"""
from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

players = {}
scores = {}
answers = {}

game_started = False
current_question = 0
question_start_time = 0

questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "C"
    },
    {
        "question": "What is 2 + 2?",
        "choices": ["3", "4", "5", "6"],
        "answer": "B"
    }
]

# ---------------- UI ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- JOIN ----------------
@app.route("/join", methods=["POST"])
def join():
    username = request.json["username"]

    if username not in players:
        players[username] = True
        scores[username] = 0

    return jsonify({"status": "joined"})

# ---------------- START GAME (HOST) ----------------
@app.route("/start", methods=["POST"])
def start():
    global game_started, question_start_time, current_question

    game_started = True
    current_question = 0
    question_start_time = time.time()

    return jsonify({"status": "started"})

# ---------------- GAME STATE (SYNC FOR ALL PLAYERS) ----------------
@app.route("/state")
def state():
    global current_question, question_start_time

    if not game_started:
        return jsonify({
            "status": "waiting",
            "players": list(players.keys())
        })

    if current_question >= len(questions):
        return jsonify({
            "status": "gameover",
            "scores": scores
        })

    q = questions[current_question]

    time_left = max(0, 10 - int(time.time() - question_start_time))

    return jsonify({
        "status": "playing",
        "question_number": current_question + 1,
        "question": q["question"],
        "choices": q["choices"],
        "time_left": time_left,
        "scores": scores,
        "players": list(players.keys())
    })

# ---------------- ANSWER ----------------
@app.route("/answer", methods=["POST"])
def answer():
    username = request.json["username"]
    choice = request.json["choice"]

    # only first answer counts
    if username not in answers:
        elapsed = time.time() - question_start_time
        answers[username] = (choice, elapsed)

    return jsonify({"status": "received"})

# ---------------- NEXT QUESTION ----------------
@app.route("/next", methods=["POST"])
def next_question():
    global current_question, answers, question_start_time

    correct = questions[current_question]["answer"]

    for user, (choice, t) in answers.items():
        if choice == correct:
            scores[user] += max(0, int(10 - t))

    answers = {}
    current_question += 1
    question_start_time = time.time()

    return jsonify({"status": "next"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)