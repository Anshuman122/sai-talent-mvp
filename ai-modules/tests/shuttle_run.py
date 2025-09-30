import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse
from scipy.signal import find_peaks

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks

def analyze_shuttle_run(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a 4x10m shuttle run video."""
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
            l_hip_x = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x
            r_hip_x = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x
            row['body_center_x'] = (l_hip_x + r_hip_x) / 2
        else:
            row['body_center_x'] = np.nan
        frame_data_list.append(row)
            
    cap.release()
    pose.close()

    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')
    if frame_data.empty or frame_data['body_center_x'].isnull().all():
        raise ValueError("Could not detect a person in the video.")

    
    x_pos = frame_data['body_center_x']
    
    peaks, _ = find_peaks(x_pos, prominence=0.1, distance=video_props.fps * 0.5)
    troughs, _ = find_peaks(-x_pos, prominence=0.1, distance=video_props.fps * 0.5)
    
    
    turns = sorted(list(np.concatenate([peaks, troughs])))
    
    if len(turns) < 3: 
        raise ValueError(f"Could not detect enough turns for a shuttle run. Found only {len(turns)}.")
    
    
    start_frame_idx = 0

    end_frame_idx = turns[2] 
                           
    total_time_s = (end_frame_idx - start_frame_idx) / video_props.fps
    
    turn_frames = [start_frame_idx] + turns[:3] + [end_frame_idx] 
    lap_frames = np.diff(turn_frames)
    lap_times_ms = [int((f / video_props.fps) * 1000) for f in lap_frames]

    metrics = {
        "total_time_ms": int(total_time_s * 1000),
        "lap_times_ms": lap_times_ms[:4] 
    }

    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="shuttle_run",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.88,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a shuttle run video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_shuttle_run(args.video_path)
        print("Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"Analysis Failed: {e}")

