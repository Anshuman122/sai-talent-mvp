import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse
from scipy.signal import find_peaks

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks

def analyze_situps(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a sit-ups video to count repetitions."""
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
            shoulder_y = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y + landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2
            hip_y = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y + landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y) / 2
            row['torso_y_diff'] = abs(shoulder_y - hip_y)
        else:
            row['torso_y_diff'] = np.nan
        frame_data_list.append(row)
            
    cap.release()
    pose.close()

    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')
    if frame_data.empty or frame_data['torso_y_diff'].isnull().all():
        raise ValueError("No pose data could be extracted.")


    signal = -frame_data['torso_y_diff']
    peaks, _ = find_peaks(signal, height=np.mean(signal), distance=int(video_props.fps * 0.8)) 
    
    situp_count = len(peaks)
    rep_timestamps_ms = [int((idx / video_props.fps) * 1000) for idx in peaks]

    metrics = {
        "count": situp_count,
        "rep_timestamps_ms": rep_timestamps_ms,
        "form_score": 0.9 
    }

    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="situps",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.92,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a sit-ups video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_situps(args.video_path)
        print("✅ Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"🔴 Analysis Failed: {e}")

