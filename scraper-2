import requests
import pandas as pd
import time

BASE_URL = "https://mftplus.com/ajax/default/calendar"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://mftplus.com/calendar"
}

# لیست دپارتمان‌ها به صورت دستی
groups = [
    {"key": "health", "title": "دانش سلامت"},
    {"key": "finance", "title": "علوم مالی و حسابداری"},
    {"key": "engineering", "title": "علوم مهندسی"},
    {"key": "it", "title": "فناوری اطلاعات و ارتباطات"},
    {"key": "management", "title": "مدیریت و کسب و کار"}
]

print("\n================ Available Departments ================\n")
for g in groups:
    print(f"{g['key']:15} | {g['title']}")
print("\n=======================================================\n")

target_dep = input("Enter the 'key' of department to filter: ")

all_courses = []
skip = 0
batch_size = 9

while True:
    payload = {
        "need": "search",
        "term": "",
        "sort": "",
        "skip": skip,
        "pSkip": 0,
        "type": "all",
        "group": target_dep
    }

    response = requests.post(BASE_URL, headers=headers, data=payload)
    response.raise_for_status()

    data = response.json()
    if not data:
        break

    print(f"Fetched {len(data)} courses for dept={target_dep}, skip={skip}")

    for item in data:
        # لینک واقعی سایت به دوره
        if item.get("lessonId") and item.get("lessonUrl"):
            course_link = f"https://mftplus.com/lesson/{item['lessonId']}/{item['lessonUrl']}"
        else:
            course_link = ""

        all_courses.append({
            "title": item.get("title", ""),
            "department": item.get("dep", ""),
            "center": item.get("center", ""),
            "teacher": item.get("author", ""),
            "start_date": item.get("start", ""),
            "end_date": item.get("end", ""),
            "min_cost": item.get("minCost", ""),
            "max_cost": item.get("maxCost", ""),
            "days": " | ".join(item.get("days", [])),
            "course_link": course_link
        })

    skip += batch_size
    time.sleep(0.5)

# ذخیره CSV
df = pd.DataFrame(all_courses)
filename = f"mft_courses_{target_dep}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"\n✅ Done! Saved {len(df)} courses to {filename}")