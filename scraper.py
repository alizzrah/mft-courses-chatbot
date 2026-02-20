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

# === 1) گرفتن لیست دپارتمان‌ها ===
group_params = {"need": "group"}
res = requests.get(BASE_URL, headers=headers, params=group_params)
res.raise_for_status()
groups = res.json()

print("Available departments:")
for g in groups:
    print(f"{g['key']}: {g['title']}")

# === 2) انتخاب دپارتمان ===
target_dep = input("\nEnter the 'key' of department to filter: ")

# === 3) گرفتن دوره‌ها برای آن دپارتمان ===
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
        "group": target_dep  # این فیلتر گروه هست
    }

    response = requests.post(BASE_URL, headers=headers, data=payload)
    response.raise_for_status()

    data = response.json()
    if not data:
        break

    print(f"Fetched {len(data)} courses for dept={target_dep}, skip={skip}")
    for item in data:
        all_courses.append({
            "title": item["title"],
            "department": item["dep"],
            "center": item["center"],
            "teacher": item["author"],
            "start_date": item["start"],
            "end_date": item["end"],
            "min_cost": item["minCost"],
            "max_cost": item["maxCost"],
            "days": " | ".join(item.get("days", []))
        })

    skip += batch_size
    time.sleep(0.5)

# === ذخیره فایل CSV ===
df = pd.DataFrame(all_courses)
filename = f"mft_courses_{target_dep}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"\n✅ Done! Saved {len(df)} courses to {filename}")
