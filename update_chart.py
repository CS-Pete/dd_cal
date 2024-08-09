import schedule
import time
import requests

def update_chart():
    response = requests.get('http://localhost:5000/get_progress')
    data = response.json()
    print(f"Updated at {time.strftime('%Y-%m-%d %H:%M:%S')}: {data}")

# Schedule the job to run once per day at midnight
schedule.every().day.at("00:00").do(update_chart)

while True:
    schedule.run_pending()
    time.sleep(1)
