import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks
from .height import get_height

def analyze_broad_jump(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a broad jump video to measure distance."""
    cap, video_props = load_video_properties(video_path)
    if not cap:
        raise ValueError("Could not open video file.")

    pose = initialize_pose_model()
    
    frame_data_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        row = {'frame_index': int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1}
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            row['left_ankle_x'] = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x
            row['left_ankle_y'] = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y
            row['left_shoulder_y'] = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y
        else:
            row['left_ankle_x'] = row['left_ankle_y'] = row['left_shoulder_y'] = np.nan

        frame_data_list.append(row)
        
    cap.release()
    pose.close()

    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')

    
    if frame_data.empty or frame_data['left_ankle_y'].isnull().all():
        raise ValueError("Could not detect a person in the video.")
        
    
    takeoff_frame_idx = np.argmin(np.gradient(frame_data['left_ankle_y']))
    
    
    landing_frame_idx = takeoff_frame_idx + np.argmax(frame_data['left_ankle_y'][takeoff_frame_idx:])
    

    takeoff_x_norm = frame_data.loc[takeoff_frame_idx, 'left_ankle_x']
    landing_x_norm = frame_data.loc[landing_frame_idx, 'left_ankle_x']
    distance_norm = abs(landing_x_norm - takeoff_x_norm)

    distance_cm = 0
    athlete_height_cm = get_height()
    if athlete_height_cm:
        
        person_height_norm = abs(frame_data['left_ankle_y'].mean() - frame_data['left_shoulder_y'].mean())
        if person_height_norm > 0:
            
            pixel_height = person_height_norm * video_props.height
            cm_per_pixel_y = athlete_height_cm / pixel_height
            cm_per_pixel_x = cm_per_pixel_y 
            
            distance_pixels = distance_norm * video_props.width
            distance_cm = distance_pixels * cm_per_pixel_x

    metrics = {
        "distance_cm": round(distance_cm, 2),
        "takeoff_frame": int(takeoff_frame_idx),
        "landing_frame": int(landing_frame_idx)
    }

    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="broad_jump",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.85,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a broad jump video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_broad_jump(args.video_path)
        print("✅ Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"🔴 Analysis Failed: {e}")

