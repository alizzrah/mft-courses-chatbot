import pandas as pd
import json

# === 1) خواندن CSV دوره‌ها ===
csv_file = ".\mft_courses_it.csv"  # جایگزین کنید با نام فایل CSV شما
df = pd.read_csv(csv_file)

# === 2) تعریف سوالات پایه برای هر Intent ===
faq_template = {
    "course_start_date": [
        "دوره {title} کی شروع می‌شود؟",
        "شروع دوره {title} چه زمانی است؟",
        "می‌خوام بدونم این دوره کی شروع میشه"
    ],
    "course_end_date": [
        "پایان دوره {title} کیه؟",
        "دوره {title} تا چه زمانی ادامه دارد؟",
        "چه زمانی این دوره تمام می‌شود؟"
    ],
    "course_teacher": [
        "مدرس دوره {title} کیه؟",
        "این دوره رو چه کسی تدریس می‌کنه؟",
        "استاد دوره {title} کیه؟"
    ],
    "course_price": [
        "قیمت دوره {title} چقدره؟",
        "این دوره {title} چه هزینه‌ای داره؟",
        "هزینه ثبت‌نام در {title} چقدره؟"
    ],
    "course_link": [
        "چطور می‌تونم ثبت‌نام کنم؟",
        "لینک دوره {title} چیه؟",
        "می‌خوام به صفحه ثبت‌نام {title} برم"
    ],
    "course_days": [
        "روزهای برگزاری {title} کدوم‌ها هستن؟",
        "دوره {title} چه روزهایی برگزار میشه؟"
    ],
    "course_center": [
        "محل برگزاری {title} کجاست؟",
        "این دوره در کدام مرکز برگزار می‌شود؟"
    ]
}

# === 3) ساخت دیتاست FAQ برای هر دوره ===
faq_dataset = []

for _, row in df.iterrows():
    course_data = {
        "title": row["title"],
        "start_date": row.get("start_date", ""),
        "end_date": row.get("end_date", ""),
        "teacher": row.get("teacher", ""),
        "min_cost": row.get("min_cost", ""),
        "max_cost": row.get("max_cost", ""),
        "days": row.get("days", ""),
        "center": row.get("center", ""),
        "link": row.get("link", "")
    }

    for intent, questions in faq_template.items():
        faq_dataset.append({
            "intent": intent,
            "questions": [q.format(**course_data) for q in questions],
            "answer": ""
        })
        
        # پاسخ‌ها رو هم بر اساس intent بسازید
        if intent == "course_start_date":
            faq_dataset[-1]["answer"] = f"دوره {course_data['title']} از {course_data['start_date']} شروع می‌شود. لینک ثبت‌نام: {course_data['link']}"
        elif intent == "course_end_date":
            faq_dataset[-1]["answer"] = f"دوره {course_data['title']} تا {course_data['end_date']} ادامه دارد."
        elif intent == "course_teacher":
            faq_dataset[-1]["answer"] = f"مدرس دوره {course_data['title']}، {course_data['teacher']} است."
        elif intent == "course_price":
            faq_dataset[-1]["answer"] = f"هزینه ثبت‌نام در دوره {course_data['title']} بین {course_data['min_cost']} تا {course_data['max_cost']} تومان است."
        elif intent == "course_link":
            faq_dataset[-1]["answer"] = f"برای ثبت‌نام در {course_data['title']} می‌توانید از این لینک استفاده کنید: {course_data['link']}"
        elif intent == "course_days":
            faq_dataset[-1]["answer"] = f"دوره {course_data['title']} در روزهای {course_data['days']} برگزار می‌شود."
        elif intent == "course_center":
            faq_dataset[-1]["answer"] = f"این دوره در مرکز {course_data['center']} برگزار می‌شود."

# === 4) ذخیره به فایل JSON ===
with open("faq_dataset.json", "w", encoding="utf-8") as f:
    json.dump(faq_dataset, f, ensure_ascii=False, indent=2)

print(f"✅ Done! FAQ dataset with {len(faq_dataset)} entries saved to faq_dataset.json")