import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np
import asyncio
import json
import time
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection

pose_detector = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
face_mesh_detector = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=5)
face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

async def analyze_frame_async(rgb_frame):
    """Run all analysis tasks concurrently for one frame."""

    async def detect_faces():
        """ Detect faces in the frame. """
        return await asyncio.to_thread(lambda: face_detector.process(rgb_frame))

    async def analyze_emotion():
        """ Analyze emotion in the frame. """
        def _emotion():
            """ Use DeepFace to analyze emotion. """
            try:
                analysis = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
                return analysis[0]['dominant_emotion']
            except Exception:
                return "unknown"
        return await asyncio.to_thread(_emotion)

    async def analyze_posture():
        """ Analyze posture in the frame. """
        def _pose():
            """ Use MediaPipe to analyze posture. """
            pose_results = pose_detector.process(rgb_frame)
            if pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark
                shoulder_y = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y +
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2
                nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
                return "upright" if nose_y < shoulder_y else "slouching"
            return "unknown"
        return await asyncio.to_thread(_pose)

    async def analyze_eye_contact():
        """ Analyze eye contact in the frame. """
        def _eye():
            """ Use MediaPipe Face Mesh to analyze eye contact. """
            results = face_mesh_detector.process(rgb_frame)
            return 1 if results.multi_face_landmarks else 0
        return await asyncio.to_thread(_eye)
    
    face_result, emotion_result, posture_result, eye_contact_result = await asyncio.gather(
        detect_faces(), analyze_emotion(), analyze_posture(), analyze_eye_contact()
    )

    humans = len(face_result.detections) if face_result.detections else 0
    return humans, emotion_result, posture_result, eye_contact_result

def analyze_candidate_video(video_path: str | None, frame_interval=30) -> str | None:
    """Analyze candidate video for behavioral metrics.
    Args:
        video_path (str | None): Path to the input video file.
    Returns:
        str | None: JSON string with analysis results.
    """
    
    if video_path is None:
        return None
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotions = []
    posture_status = []
    eye_contact_scores = []
    human_counts = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            humans, emotion, posture, eye_contact = asyncio.run(analyze_frame_async(rgb_frame))
            human_counts.append(humans)
            emotions.append(emotion)
            posture_status.append(posture)
            eye_contact_scores.append(eye_contact)

        frame_count += 1

    cap.release()

    avg_eye_contact = np.mean(eye_contact_scores) if eye_contact_scores else 0
    avg_humans = int(round(np.mean(human_counts))) if human_counts else 0
    posture_summary = max(set(posture_status), key=posture_status.count) if posture_status else "unknown"
    unique_emotions = list(set(emotions))

    posture_score = 1.0 if posture_summary == "upright" else 0.5 if posture_summary == "slouching" else 0.3
    emotion_score = sum(e in ["happy", "neutral", "confident"] for e in emotions) / len(emotions) if emotions else 0
    overall_score = round(((avg_eye_contact * 40) + (posture_score * 30) + (emotion_score * 30)), 2)

    result = {
        "noOfHuman": avg_humans,
        "posture": posture_summary,
        "eye_contact_score": round(float(avg_eye_contact), 2),
        "emotion": unique_emotions,
        "overallBehavioralScore": overall_score
    }

    return json.dumps(result, indent=2)

# remove the example usage comment block before deploying, testing and production.
# if __name__ == "__main__":
#     """Example usage of analyze_candidate_video function."""
#     video_path = "input.mp4"
#     start_time = time.time()
#     report = analyze_candidate_video(video_path)
#     end_time = time.time()
#     print(f"Analysis Time: {end_time - start_time:.2f} seconds")
#     print(report)