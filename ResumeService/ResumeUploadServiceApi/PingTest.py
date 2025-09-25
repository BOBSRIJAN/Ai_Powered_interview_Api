import requests
from apscheduler.schedulers.background import BackgroundScheduler

def ping_server():
    try:
        url = "https://resumeservice.onrender.com/resumeanalyzer/api/v1/user/"
        response = requests.get(url)
        print("Pinged:", response.status_code)
    except Exception as e:
        print("Ping failed:", e)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ping_server, 'interval', minutes=10)
    scheduler.start()