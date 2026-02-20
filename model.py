import pandas as pd
import json
from hazm import Normalizer, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === 1) بارگذاری داده‌ها ===

# فایل CSV دوره‌ها
csv_file = "mft_courses_it.csv"
df_courses = pd.read_csv(csv_file)

# فایل FAQ
faq_file = "faq_dataset.json"
with open(faq_file, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# === 2) نرمال‌سازی متن‌ها ===
normalizer = Normalizer()

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = normalizer.normalize(text)
    return text

# نرمال‌سازی سوالات و پاسخ‌ها
corpus_texts = []
corpus_answers = []

# --- FAQ ---
for faq in faq_data:
    answer = faq.get("answer", "")
    for q in faq.get("questions", []):
        corpus_texts.append(normalize_text(q))
        corpus_answers.append(answer)

# --- دوره‌ها از CSV ---
for _, row in df_courses.iterrows():
    # ساخت سوالات فرضی بر اساس ستون‌های CSV
    course_title = row.get("title", "")
    if pd.isna(course_title):
        continue
    
    # اضافه کردن نمونه سوالات
    questions = [
        f"{course_title} کی شروع می‌شود؟",
        f"{course_title} چه روزهایی برگزار می‌شود؟",
        f"{course_title} چه کسی تدریس می‌کند؟",
        f"قیمت {course_title} چقدر است؟",
        f"چطور می‌توانم ثبت‌نام کنم؟"
    ]
    
    # پاسخ‌ها
    answers = [
        f"تاریخ شروع {course_title}: {row.get('start_date', 'نامشخص')}",
        f"روزهای برگزاری {course_title}: {row.get('days', 'نامشخص')}",
        f"مدرس {course_title}: {row.get('teacher', 'نامشخص')}",
        f"هزینه {course_title}: {row.get('min_cost', '-')}-{row.get('max_cost', '-')}",
        f"لینک ثبت‌نام: {row.get('course_link', 'نامشخص')}"
    ]
    
    for q, a in zip(questions, answers):
        corpus_texts.append(normalize_text(q))
        corpus_answers.append(a)

# === 3) محاسبه TF-IDF ===
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus_texts)

# === 4) حلقه‌ی چت بات ===
print("\n🤖 چت بات مجتمع فنی آماده است! برای خروج 'خروج' را تایپ کنید.\n")

while True:
    user_input = input("شما: ")
    if user_input.strip() in ["خروج", "exit"]:
        print("👋 خداحافظ!")
        break
    
    user_norm = normalize_text(user_input)
    user_vec = vectorizer.transform([user_norm])
    
    # محاسبه شباهت کسینوس
    sims = cosine_similarity(user_vec, tfidf_matrix)
    best_idx = sims.argmax()
    
    if sims[0, best_idx] < 0.1:
        print("🤖 متاسفم، پاسخی پیدا نکردم.")
    else:
        print(f"🤖 {corpus_answers[best_idx]}")