import requests
import time
import webbrowser

# This matches the default address and port of your Flask server
SERVER_URL = "http://127.0.0.1:5000"

def ClientMain():
    print("Opening the game in your web browser...")
    webbrowser.open(SERVER_URL)
    username = input("What is your username? ")
    
    # 1. Join the Game
    try:
        response = requests.post(f"{SERVER_URL}/join", json={"username": username})
        if response.status_code == 200:
            print("✅ Successfully joined the game! Waiting for the host to start...")
        else:
            print("❌ Failed to join.")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Is KahootServer.py running?")
        return

    last_question = 0

    # 2. Game Loop (Polling the server for the current state)
    while True:
        try:
            # Check the /state endpoint you created
            state_resp = requests.get(f"{SERVER_URL}/state").json()
            status = state_resp.get("status")

            if status == "waiting":
                # Game hasn't started yet, wait 1 second and check again
                time.sleep(1)
                continue
            
            elif status == "playing":
                current_q = state_resp["question_number"]
                
                # If the server has moved to a new question, display it
                if current_q != last_question:
                    print(f"\n--- Question {current_q} ---")
                    print(state_resp['question'])
                    
                    # Print the choices
                    for idx, choice in enumerate(state_resp['choices']):
                        # Convert index 0,1,2,3 to A,B,C,D
                        letter = chr(65 + idx) 
                        print(f"[{letter}] {choice}")
                    
                    # Get the user's answer
                    answer = input("\nEnter answer (A/B/C/D): ")
                    
                    # Send the answer to your /answer route
                    requests.post(f"{SERVER_URL}/answer", json={
                        "username": username,
                        "choice": answer.upper()
                    })
                    print("Answer submitted! Waiting for the next question...")
                    
                    # Update our tracker so we don't prompt for this question again
                    last_question = current_q
            
            elif status == "gameover":
                print("\n🏁 Game Over! Final Scores:")
                scores = state_resp.get("scores", {})
                
                # Sort and print scores
                for user, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    print(f" - {user}: {score} points")
                break

            # Pause briefly before checking the state again to avoid spamming the server
            time.sleep(1)

        except Exception as e:
            print(f"Lost connection to server: {e}")
            break

if __name__ == "__main__":
    ClientMain()
