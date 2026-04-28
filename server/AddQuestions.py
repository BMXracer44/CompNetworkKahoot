import json
import os

FILE_NAME = "questions.json"

def main():
    print("📝 Kahoot Question Adder 📝")
    print("-" * 30)
    
    question_text = input("Enter the question: ")
    
    choices = []
    for letter in ['A', 'B', 'C', 'D']:
        choices.append(input(f"Enter choice {letter}: "))
        
    correct_answer = ""
    while correct_answer not in ['A', 'B', 'C', 'D']:
        correct_answer = input("Which is the correct answer (A/B/C/D)? ").strip().upper()
    
    new_question = {
        "question": question_text,
        "choices": choices,
        "answer": correct_answer
    }
    
    # Load existing questions if the file exists
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            try:
                questions = json.load(f)
            except json.JSONDecodeError:
                questions = [] # If file is empty or corrupted
    else:
        questions = []
        
    # Add the new question and save it
    questions.append(new_question)
    
    with open(FILE_NAME, "w") as f:
        json.dump(questions, f, indent=4)
        
    print(f"\n✅ Question added! You now have {len(questions)} questions in your bank.")

if __name__ == "__main__":
    # Loop so you can add multiple quickly
    while True:
        main()
        cont = input("\nAdd another question? (y/n): ").lower()
        if cont != 'y':
            break