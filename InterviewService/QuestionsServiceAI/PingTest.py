import requests
from apscheduler.schedulers.background import BackgroundScheduler

def ping_server():
    try:
        url = "http://127.0.0.1:8000/InterviewService/V1/isActive/"
        response = requests.get(url)
        print("Pinged:", response.status_code)
    except Exception as e:
        print("Ping failed:", e)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ping_server, 'interval', minutes=1)
    scheduler.start()
