import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks

def analyze_sprint_30m(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a 30m sprint video, assuming start and finish lines are the screen edges."""
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
            
            row['nose_x'] = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.NOSE.value].x
        else:
            row['nose_x'] = np.nan
        frame_data_list.append(row)
            
    cap.release()
    pose.close()

    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')
    if frame_data.empty or frame_data['nose_x'].isnull().all():
        raise ValueError("Could not detect a person in the video.")


    start_frame_series = frame_data[frame_data['nose_x'] > 0.05]
    start_frame_idx = start_frame_series.index[0] if not start_frame_series.empty else -1


    finish_frame_series = frame_data[frame_data['nose_x'] > 0.95]
    finish_frame_idx = finish_frame_series.index[0] if not finish_frame_series.empty else -1

    if start_frame_idx == -1 or finish_frame_idx == -1 or finish_frame_idx <= start_frame_idx:
        raise ValueError("Could not determine a valid start and finish time based on screen crossing.")

    time_s = (finish_frame_idx - start_frame_idx) / video_props.fps
    

    split_10m_frame_idx_series = frame_data[frame_data['nose_x'] > (0.05 + (0.95 - 0.05) / 3)]
    split_10m_frame_idx = split_10m_frame_idx_series.index[0] if not split_10m_frame_idx_series.empty else -1
    split_time_s = (split_10m_frame_idx - start_frame_idx) / video_props.fps if split_10m_frame_idx != -1 else 0

    metrics = {
        "time_ms": int(time_s * 1000),
        "split_10m_ms": int(split_time_s * 1000),
        "average_speed_m_s": round(30 / time_s, 2) if time_s > 0 else 0
    }
    
    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="sprint_30m",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.9,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a 30m sprint video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_sprint_30m(args.video_path)
        print("✅ Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"🔴 Analysis Failed: {e}")

