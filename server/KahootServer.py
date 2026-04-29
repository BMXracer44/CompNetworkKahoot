from flask import Flask, request, jsonify, render_template
import time
import webbrowser
import threading
import json 
import os 

app = Flask(__name__)

players = {}
scores = {}
answers = {}
questions = [] # Starts empty, gets populated when game starts

game_started = False
question_state = "playing"
current_question = 0
question_start_time = 0

# ---------------- VIEWS ----------------
@app.route("/")
def player_view():
    return render_template("player.html")

@app.route("/host")
def host_view():
    return render_template("host.html")

# ---------------- API ENDPOINTS ----------------
@app.route("/join", methods=["POST"])
def join():
    username = request.json["username"]
    if username not in players:
        players[username] = True
        scores[username] = 0
    return jsonify({"status": "joined"})

@app.route("/start", methods=["POST"])
def start():
    global game_started, question_start_time, current_question, answers, question_state, questions
    
    # Load questions dynamically every time a new game starts
    if os.path.exists("server/questions.json"):
        with open("server/questions.json", "r") as f:
            questions = json.load(f)
    else:
        questions = [{"question": "No questions.json found!", "choices": ["A", "B", "C", "D"], "answer": "A"}]

    game_started = True
    current_question = 0
    answers = {}
    question_state = "playing"
    question_start_time = time.time()
    return jsonify({"status": "started"})

@app.route("/state")
def state():
    global question_state
    
    if not game_started:
        return jsonify({"status": "waiting", "players": list(players.keys())})

    if current_question >= len(questions):
        return jsonify({"status": "gameover", "scores": scores})

    q = questions[current_question]
    time_left = max(0, 10 - int(time.time() - question_start_time))

    all_answered = len(players) > 0 and len(answers) >= len(players)

    if (time_left == 0 or all_answered) and question_state == "playing":
        correct = q["answer"]
        for user, (choice, t) in answers.items():
            if choice == correct:
                scores[user] += max(0, int(10 - t))
        question_state = "revealed"

    client_answers = {}
    if question_state == "revealed":
        client_answers = {user: {"choice": ans[0], "time": ans[1]} for user, ans in answers.items()}

    return jsonify({
        "status": question_state,
        "question_number": current_question + 1,
        "question": q["question"],
        "choices": q["choices"],
        "time_left": 0 if question_state == "revealed" else time_left,
        "scores": scores,
        "players": list(players.keys()),
        "correct_answer": q["answer"] if question_state == "revealed" else None,
        "answers": client_answers,
        "answers_count": len(answers),
        # NEW: Tell the client if this is the final question
        "is_last_question": current_question == len(questions) - 1 
    })

@app.route("/answer", methods=["POST"])
def answer():
    username = request.json["username"]
    choice = request.json["choice"]
    
    if question_state != "playing":
         return jsonify({"status": "late"})

    if username not in answers:
        elapsed = time.time() - question_start_time
        answers[username] = (choice, elapsed)

    return jsonify({"status": "received"})

@app.route("/next", methods=["POST"])
def next_question():
    global current_question, answers, question_start_time, question_state
    
    answers = {}
    current_question += 1
    question_state = "playing"
    question_start_time = time.time()
    
    return jsonify({"status": "next"})

# ---------------- RUN ----------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/host")

if __name__ == "__main__":
    print("🚀 Starting Kahoot Server...")
    print("Host Dashboard: http://127.0.0.1:5000/host")
    print("Player Join: http://127.0.0.1:5000/")
    
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True, use_reloader=False)