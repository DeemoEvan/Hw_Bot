import pandas as pd
import requests
import re
import time
import random

API_KEY = 'AIzaSyCZA88e6Y9i4LuPMBBmTU9GTYsYw_e_l5Y'
API_URL = (
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'
)

questions_df = pd.read_csv('mmlu_submit.csv')

def generate_answer(question_text, answer_options, subject_domain):
    """Generate an answer using the Gemini API based on the given question and options."""
    system_prompt = (
        f'You are a professional in the field of {subject_domain}. I have the following question which I need you to solve:\n\n'
        f'{question_text}\n\n'
        f'Which of the following is the correct answer?\n\n'
        f'A) {answer_options["A"]}\nB) {answer_options["B"]}\nC) {answer_options["C"]}\nD) {answer_options["D"]}\n\n'
        f'Breifly describe how do you get your answer. You must also respond strictly in this format: Answer: <A/B/C/D>\n\n'
        f'If you are ready, please provide the answer to the question.\n\n'
        'If you do not know the answer, please respond with "I do not know the answer."'
    )
    user_prompt = 'Answer: '

    try:
        reply = requests.post(
            API_URL,
            headers={'Content-Type': 'application/json'},
            json={
                "contents": [{"parts": [{"text": system_prompt + user_prompt}]}],
                "generationConfig": {
                    "temperature": 0,
                    "maxOutputTokens": 2000,
                }
            }
        )

        reply_json = reply.json()

        if 'candidates' not in reply_json:
            print("❌ API Error:", reply_json)
            return 'A'

        answer_text = reply_json['candidates'][0]['content']['parts'][0]['text'].strip()
        match = re.search(r'Answer:\s*([A-D])', answer_text, re.IGNORECASE)

        if match:
            print("✅ Complete API reply:", answer_text)
            return match.group(1)
        else:
            if("I do not know the answer." in answer_text):
                print("⚠️ Warning: Do not know the answer.")
                random_answer = random.choice(['A', 'B', 'C', 'D'])
                print(f"🔮 Randomly selected answer: {random_answer}")
                return random_answer

    except Exception as error:
        print("❌ Exception Error:", error)
        return 'A'


def main():
    """Main function to generate answers for all questions and save the results."""
    predictions = []
    total_questions = len(questions_df)
    print(f"📚 Total questions: {total_questions}")

    for index, row in questions_df.iterrows():
        answer_options = {'A': row['A'], 'B': row['B'], 'C': row['C'], 'D': row['D']}
        subject_domain = row['task']
        predicted_answer = generate_answer(row['input'], answer_options, subject_domain)

        predictions.append({'ID': row['Unnamed: 0'], 'target': predicted_answer})

        print(f"📝 Question {index + 1}/{total_questions} | Generated Answer: {predicted_answer}")
        time.sleep(5)

    submission_df = pd.DataFrame(predictions)
    submission_df.to_csv('submission_gemini_flash2.csv', index=False)

    print(f"🔎 Generation complete! Total questions: {total_questions}, Total answers generated: {len(predictions)}")


if __name__ == "__main__":
    main()