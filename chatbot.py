import json
from difflib import get_close_matches
from typing import List

def load_chatbot(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_chatbot(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chatbot():
    chatbot: dict = load_chatbot('chatbot.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in chatbot["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, chatbot)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                chatbot["questions"].append({"question": user_input, "answer": new_answer})
                save_chatbot('chatbot.json', chatbot)
                print('Bot: Thank you!')

if __name__ == '__main__':
    chatbot()
