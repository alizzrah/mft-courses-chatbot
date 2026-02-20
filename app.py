from flask import Flask, render_template, request
import pandas as pd
import json
from hazm import Normalizer, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === آماده‌سازی داده‌ها ===
# CSV دوره‌ها
courses_df = pd.read_csv("mft_courses_it.csv", encoding="utf-8-sig")
courses_df.fillna("", inplace=True)

# FAQ
with open("faq_dataset.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Hazm normalizer
normalizer = Normalizer()

# لیست سوالات و جواب‌ها از FAQ
faq_questions = []
faq_answers = []
for item in faq_data:
    for q in item["questions"]:
        faq_questions.append(normalizer.normalize(q))
        faq_answers.append(item["answer"])

# vectorizer برای جستجوی cosine
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)

# === وب اپ Flask ===
app = Flask(__name__)

def get_response(user_question):
    question_norm = normalizer.normalize(user_question)
    q_vec = vectorizer.transform([question_norm])
    sim_scores = cosine_similarity(q_vec, faq_vectors)
    idx = sim_scores.argmax()
    
    # اگه شباهت کافی هست، جواب FAQ بده
    if sim_scores[0, idx] > 0.2:
        answer = faq_answers[idx]
    else:
        answer = "متاسفم، پاسخ مناسب پیدا نشد."

    # بررسی CSV برای دوره‌ها
    for _, row in courses_df.iterrows():
        title_norm = normalizer.normalize(row["title"])
        if title_norm in question_norm:
            answer += f"\n📌 اطلاعات دوره:\n- لینک ثبت‌نام: {row['course_link']}\n- شروع: {row['start_date']}\n- پایان: {row['end_date']}\n- مدرس: {row['teacher']}\n- روزها: {row['days']}\n- مرکز: {row['center']}\n- هزینه: {row['min_cost']} تا {row['max_cost']} تومان"
            break

    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    user_question = ""
    answer = ""
    if request.method == "POST":
        user_question = request.form.get("question")
        answer = get_response(user_question)
    return render_template("index.html", question=user_question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)