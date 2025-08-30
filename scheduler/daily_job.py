import schedule, time

def job():
    print("Scheduled job running... (Scrape, Tag, Notify)")

schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
