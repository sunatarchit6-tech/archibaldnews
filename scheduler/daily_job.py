import schedule
import time
import requests

def job():
    print("🚀 Running scheduled job to refresh news articles...")
    try:
        response = requests.post("https://archibaldnews-backend.onrender.com/news/fetch-and-cache")
        if response.status_code == 200:
            print("✅ Successfully fetched and cached articles.")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print("❌ Exception occurred during job:", str(e))

# Schedule the job for 10:00 AM every day
schedule.every().day.at("10:00").do(job)

print("📅 Scheduler started. Waiting for 10:00 AM daily task...")

while True:
    schedule.run_pending()
    time.sleep(60)
