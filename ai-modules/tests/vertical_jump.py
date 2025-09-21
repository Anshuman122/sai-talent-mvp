import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import argparse
from scipy.signal import find_peaks

from common.types import TestResult
from utils import load_video_properties, initialize_pose_model
from cheat_detection import run_all_checks
from .height import get_height 

def analyze_vertical_jump(video_path: str, athlete_id: str = "default_athlete") -> TestResult:
    """Analyzes a vertical jump video to count jumps and estimate height."""
    cap, video_props = load_video_properties(video_path)
    if not cap:
        raise ValueError("Could not open or process video file.")

    pose = initialize_pose_model()
    
    frame_data_list = []
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        row = {'frame_index': frame_idx}
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            row['left_ankle_y'] = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y
            row['right_ankle_y'] = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y
            row['left_shoulder_y'] = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y
            row['right_shoulder_y'] = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y
        else:

            row['left_ankle_y'] = row['right_ankle_y'] = row['left_shoulder_y'] = row['right_shoulder_y'] = np.nan
        
        frame_data_list.append(row)
        frame_idx += 1
        
    cap.release()
    pose.close()

    frame_data = pd.DataFrame(frame_data_list).interpolate(method='linear', limit_direction='both')
    

    if frame_data.empty or frame_data['left_ankle_y'].isnull().all():
        raise ValueError("Could not detect a person in the video.")


    inverted_y = -((frame_data['left_ankle_y'] + frame_data['right_ankle_y']) / 2)
    peaks, _ = find_peaks(inverted_y, height=np.mean(inverted_y), distance=int(video_props.fps * 0.5))
    num_jumps = len(peaks)

    max_jump_height_cm = 0
    if num_jumps > 0:
        
        highest_peak_idx = peaks[np.argmax(inverted_y[peaks])]
        
        
        search_range_start = max(0, highest_peak_idx - int(video_props.fps))
        takeoff_idx = search_range_start + np.argmin(inverted_y[search_range_start:highest_peak_idx])
        
        jump_height_normalized = inverted_y[highest_peak_idx] - inverted_y[takeoff_idx]
        
        
        athlete_height_cm = get_height()
        if athlete_height_cm:
            
            person_height_norm = abs(frame_data['left_ankle_y'].mean() - frame_data['left_shoulder_y'].mean())
            if person_height_norm > 0:
                pixel_to_cm_ratio = athlete_height_cm / person_height_norm
                max_jump_height_cm = jump_height_normalized * pixel_to_cm_ratio
    
    metrics = {
        "jump_count": num_jumps,
        "jump_height_cm": round(max_jump_height_cm, 2),
        "flight_time_ms": 0,
        "frames_analyzed": len(frame_data)
    }

    cheating_report = run_all_checks(video_path, frame_data)

    return TestResult(
        test_name="vertical_jump",
        athlete_id=athlete_id,
        metrics=metrics,
        valid=True,
        confidence=0.9,
        cheat_flags=cheating_report
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze a vertical jump video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    args = parser.parse_args()
    
    try:
        result = analyze_vertical_jump(args.video_path)
        print("✅ Analysis Successful!")
        print(result.model_dump_json(indent=4))
    except Exception as e:
        print(f"🔴 Analysis Failed: {e}")

