from fastapi import FastAPI
from kafka import KafkaProducer
import json
import time
import requests
import uvicorn

app = FastAPI(title="Video Analysis Producer API")

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC_NAME = "video_analysis_request"

MAIN_USER_ID = "536739hgg7-7hjkew87-guiwrg987-gy247"
VIDEO_URL = "https://res.cloudinary.com/didiyzbnq/video/upload/v1761042637/Recording_2025-10-21_160003_wogqo2.mp4"

FIRST_SLOT_URL = "http://interview-question-service:8000/interviewservice/api/v1/initializeinterview/getfirstslotquestion"
SECOND_SLOT_URL = "http://interview-question-service:8000/interviewservice/api/v1/initializeinterview/getsecondslotquestion"


def send_to_kafka(data: dict):
    producer.send(TOPIC_NAME, value=data)
    producer.flush()


@app.post("/send-video-analysis")
def send_video_analysis_requests():
    print("API HIT: /send-video-analysis")

    first_slot_payload = {
        "userid": MAIN_USER_ID,
        "resumeurl": "https://res.cloudinary.com/didiyzbnq/raw/upload/v1752064497/resumes/Arindam%20Resume.pdf",
        "specificquestionrequirement": False,
        "subjectortopic": ["python", "java", "C"],
        "numberofquestions": 10,
        "level": "easy"
    }

    print("Sending first slot request...")
    first_response = requests.post(
        FIRST_SLOT_URL, json=first_slot_payload).json()
    print("First slot response received")

    sessionid = first_response["sessionid"]
    slot_one_questions = first_response["slotonequestions"]
    remanning = first_response["remanning"]

    print(f"Session ID: {sessionid}")
    print(f"Slot 1 Questions Count: {len(slot_one_questions)}")

    for q_no, question in enumerate(slot_one_questions, start=1):
        data = {
            "userid": MAIN_USER_ID,
            "sessionid": sessionid,
            "questionno": q_no,
            "question": question,
            "videourl": VIDEO_URL,
            "totalnumberofquestion": 10
        }
        send_to_kafka(data)
        print(f"Kafka Sent: Slot1 Q{q_no}")

    print("Waiting 1 minute before requesting second slot...")
    time.sleep(90)

    slot_two_questions = None

    while not slot_two_questions:
        print("Requesting second slot questions...")
        second_slot_payload = {
            "userid": MAIN_USER_ID,
            "sessionid": sessionid,
            "remanning": remanning,
            "level": "easy"
        }

        second_response = requests.post(
            SECOND_SLOT_URL, json=second_slot_payload).json()
        slot_two_questions = second_response.get("slottwoquestions")

        if not slot_two_questions:
            print("Slot 2 not ready, retrying in 10 seconds...")
            time.sleep(10)

    print(f"Slot 2 Questions Received: {len(slot_two_questions)}")

    start_q_no = len(slot_one_questions) + 1

    for i, question in enumerate(slot_two_questions):
        data = {
            "userid": MAIN_USER_ID,
            "sessionid": sessionid,
            "questionno": start_q_no + i,
            "question": question,
            "videourl": VIDEO_URL,
            "totalnumberofquestion": 10
        }
        send_to_kafka(data)
        print(f"Kafka Sent: Slot2 Q{start_q_no + i}")

    print("🎉 All questions sent to Kafka successfully")

    return {
        "status": "success",
        "message": "All interview questions sent to Kafka",
        "sessionid": sessionid,
        "total_questions": len(slot_one_questions) + len(slot_two_questions)
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
