""" 
Video Analysis Module
    This module analyzes a candidate's video for behavioral metrics such as emotion, posture, eye contact
    and number of humans detected.
    Returns:
        str : JSON string with analysis results.
"""
# Import Headers
import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["DEEPFACE_HOME"] = os.path.join(
    CURRENT_DIR,
    "deepfaceData"
)
import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np
import asyncio
import json
import time

# program configurations
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection

pose_detector = mp_pose.Pose(
    static_image_mode=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

face_mesh_detector = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1
)

face_detector = mp_face_detection.FaceDetection(
    min_detection_confidence=0.5
)


async def analyze_frame_async(rgb_frame, run_emotion: bool):
    """ Asynchronously analyze a single video frame for behavioral metrics. """
    
    async def detect_faces():
        """Detect faces in the RGB frame."""
        return await asyncio.to_thread(lambda: face_detector.process(rgb_frame))

    async def analyze_emotion():
        """Analyze the emotion in the RGB frame."""
        def _emotion():
            """ Helper function to analyze emotion using DeepFace. """
            try:
                analysis = DeepFace.analyze(
                    rgb_frame,
                    actions=["emotion"],
                    enforce_detection=False
                )
                return analysis[0]["dominant_emotion"]
            except Exception:
                return "unknown"
        return await asyncio.to_thread(_emotion)

    async def analyze_posture():
        """ Analyze posture in the RGB frame. """
        def _pose():
            """ Helper function to analyze posture using MediaPipe Pose. """
            results = pose_detector.process(rgb_frame)
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                shoulder_y = (lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y +
                              lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2
                nose_y = lm[mp_pose.PoseLandmark.NOSE.value].y
                return "upright" if nose_y < shoulder_y else "slouching"
            return "unknown"
        return await asyncio.to_thread(_pose)

    async def analyze_eye_contact():
        """ Analyze eye contact in the RGB frame. """
        def _eye():
            """ Helper function to analyze eye contact using MediaPipe Face Mesh. """
            results = face_mesh_detector.process(rgb_frame)
            return 1 if results.multi_face_landmarks else 0
        return await asyncio.to_thread(_eye)

    tasks = [
        detect_faces(),
        analyze_posture(),
        analyze_eye_contact()
    ]

    if run_emotion:
        tasks.append(analyze_emotion())
    results = await asyncio.gather(*tasks)

    face_result = results[0]
    posture = results[1]
    eye_contact = results[2]
    emotion = results[3] if run_emotion else None

    humans = len(face_result.detections) if face_result.detections else 0
    return humans, emotion, posture, eye_contact


def analyzeCandidateVideo(video_path: str, frame_interval: int = 60) -> str:
    """Analyze a candidate's video for behavioral metrics.
        Args:
            video_path (str): Path to the input video file.
            frame_interval (int): Interval at which frames are analyzed.
        Returns:
            str : JSON string with analysis results.
    """
    cap = cv2.VideoCapture(video_path)

    emotions = []
    posture_status = []
    eye_contact_scores = []
    human_counts = []

    frame_count = 0
    last_emotion = "unknown"
    EMOTION_INTERVAL = 180

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame = cv2.resize(rgb_frame, (320, 240))

            run_emotion = frame_count % EMOTION_INTERVAL == 0

            humans, emotion, posture, eye_contact = loop.run_until_complete(
                analyze_frame_async(rgb_frame, run_emotion)
            )

            if emotion:
                last_emotion = emotion

            human_counts.append(humans)
            emotions.append(last_emotion)
            posture_status.append(posture)
            eye_contact_scores.append(eye_contact)

        frame_count += 1

    cap.release()
    loop.close()

    avg_eye_contact = float(np.mean(eye_contact_scores)
                            ) if eye_contact_scores else 0
    avg_humans = int(round(np.mean(human_counts))) if human_counts else 0
    posture_summary = (
        max(set(posture_status), key=posture_status.count)
        if posture_status else "unknown"
    )
    unique_emotions = list(set(emotions))

    posture_score = 1.0 if posture_summary == "upright" else 0.5 if posture_summary == "slouching" else 0.3
    emotion_score = (
        sum(e in ["happy", "neutral", "confident"]
            for e in emotions) / len(emotions)
        if emotions else 0
    )

    overall_score = round(
        (avg_eye_contact * 40) + (posture_score * 30) + (emotion_score * 30),
        2
    )

    return json.dumps({
        "noOfHuman": avg_humans,
        "posture": posture_summary,
        "eye_contact_score": round(avg_eye_contact, 2) * 100,
        "emotion": unique_emotions,
        "overallBehavioralScore": overall_score
    }, indent=2)


# remove the example usage comment block before deploying or production.
# if __name__ == "__main__":
#     """Example usage of analyze_candidate_video function."""
#     video_path = "input.mp4"
#     start_time = time.time()
#     report = analyze_candidate_video(video_path)
#     end_time = time.time()
#     print(f"Analysis Time: {end_time - start_time:.2f} seconds")
#     print(report)