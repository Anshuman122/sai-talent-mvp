import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks
from .height import get_height

def analyze_medicine_ball_throw(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a medicine ball throw video to measure distance."""
    cap, video_props = load_video_properties(video_path)
    if not cap:
        raise ValueError("Could not open video file.")

    # --- Ball Tracking (Simple Color-based) ---
    # NOTE: These HSV values are for a bright green ball and will likely need tuning.
    lower_hsv = np.array([35, 100, 100])
    upper_hsv = np.array([85, 255, 255])
    ball_trajectory = []

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        center = None
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 5: 
                center = (x, y)
        
        ball_trajectory.append({'frame_index': frame_idx, 'ball_x': center[0] if center else None, 'ball_y': center[1] if center else None})
        frame_idx += 1

    cap.release()
    frame_data = pd.DataFrame(ball_trajectory).interpolate(method='linear', limit_direction='both')
    if frame_data.empty or frame_data['ball_x'].isnull().all():
        raise ValueError("Could not detect the medicine ball in the video.")

    
    velocities = np.linalg.norm(frame_data[['ball_x', 'ball_y']].diff().values, axis=1)
    release_frame_idx = np.nanargmax(velocities) if not np.isnan(velocities).all() else -1
    
    if release_frame_idx == -1:
        raise ValueError("Could not determine ball release point.")
    
    landing_frame_idx = release_frame_idx + np.nanargmax(frame_data['ball_y'][release_frame_idx:])
    
    
    release_pos = frame_data.loc[release_frame_idx, ['ball_x', 'ball_y']].values
    landing_pos = frame_data.loc[landing_frame_idx, ['ball_x', 'ball_y']].values
    distance_pixels = np.linalg.norm(landing_pos - release_pos)
    
    distance_cm = distance_pixels * 1.5

    metrics = {
        "distance_cm": round(distance_cm, 2),
        "release_velocity_m_s": 0.0, 
        "release_angle_deg": 0.0    
    }
    
    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="medicine_ball",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.75,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a medicine ball throw video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_medicine_ball_throw(args.video_path)
        print("Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"Analysis Failed: {e}")

