import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse
from scipy.signal import find_peaks

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks

def analyze_endurance_run(video_path: str, athlete_id: str = "default_athlete", distance_m: int = 800) -> TestResult:
    """Analyzes an endurance run video for time and cadence."""
    cap, video_props = load_video_properties(video_path)
    if not cap:
        raise ValueError("Could not open video file.")

    # For endurance, the main metric is time. The video duration is the result.
    total_time_s = video_props.frame_count / video_props.fps if video_props.fps > 0 else 0
    
    # AI part: Verify continuous activity by checking pose and calculating cadence
    pose = initialize_pose_model()
    
    frame_data_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        row = {'frame_index': int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1}
        if results.pose_landmarks:
            row['right_ankle_y'] = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y
            row['stride_length'] = abs(
                results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x -
                results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x
            )
        else:
            row['right_ankle_y'] = np.nan
            row['stride_length'] = np.nan
        frame_data_list.append(row)
            
    cap.release()
    pose.close()
    
    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')
    
    
    ankle_y = frame_data['right_ankle_y'].dropna()
    cadence = 0
    if not ankle_y.empty:
        
        peaks, _ = find_peaks(-ankle_y, prominence=0.01, distance=int(video_props.fps * 0.3))
    
        cadence = len(peaks) * 2 / (total_time_s / 60) if total_time_s > 0 else 0 

    
    pace_s_per_km = (total_time_s / (distance_m / 1000)) if distance_m > 0 else 0

    
    fatigue_detected = False
    stride_data = frame_data['stride_length'].dropna()
    if len(stride_data) > 20: 
        window_size = int(len(stride_data) * 0.2) 
        start_avg = stride_data.iloc[:window_size].mean()
        end_avg = stride_data.iloc[-window_size:].mean()
        if end_avg < start_avg * 0.9: 
            fatigue_detected = True

    metrics = {
        "distance_m": distance_m,
        "time_ms": int(total_time_s * 1000),
        "pace_s_per_km": round(pace_s_per_km, 2),
        "average_cadence_spm": round(cadence, 2),
        "fatigue_detected": fatigue_detected
    }

    
    confidence = 1.0 - (frame_data['right_ankle_y'].isnull().sum() / len(frame_data))
    
    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="endurance_run",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=confidence > 0.8, 
        confidence=round(confidence, 2),
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze an endurance run video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("--distance", type=int, default=800, help="Distance of the run in meters (e.g., 800 or 1600).")
    args = parser.parse_args()
    
    try:
        result = analyze_endurance_run(args.video_path, distance_m=args.distance)
        print("✅ Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"🔴 Analysis Failed: {e}")

