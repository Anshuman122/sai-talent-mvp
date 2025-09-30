
import cv2
import numpy as np
import pandas as pd
from typing import List

from .base import CheatEvent, CheatingReport

def detect_scene_changes(video_path: str, threshold: float = 30.0) -> List[CheatEvent]:
    """
    Detects abrupt scene changes by calculating the mean absolute difference
    between consecutive frames. High differences may indicate a video cut.
    """
    events = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return events
        
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return events
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_idx = 1
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        mean_diff = np.mean(diff)
        
        if mean_diff > threshold:
            events.append(CheatEvent(
                frame_index=frame_idx,
                event_type="scene_cut",
                description=f"High frame difference ({mean_diff:.2f}) detected, indicating a potential video cut.",
                severity=0.9
            ))
            
        prev_gray = gray
        frame_idx += 1
        
    cap.release()
    return events

def detect_pose_jumps(frame_data: pd.DataFrame, threshold: float = 0.15) -> List[CheatEvent]:
    """
    Detects unnatural jumps in pose landmark positions between consecutive frames.
    Large, instantaneous displacement can indicate video splicing.
    """
    events = []
    landmark_cols = [col for col in frame_data.columns if '_x' in col or '_y' in col]
    
    for i in range(1, len(frame_data)):
        prev_row = frame_data.iloc[i-1]
        curr_row = frame_data.iloc[i]
        
        displacements = []
       
        landmark_bases = set(c.rsplit('_', 1)[0] for c in landmark_cols)

        for base in landmark_bases:
            prev_pt = np.array([prev_row.get(f'{base}_x'), prev_row.get(f'{base}_y')])
            curr_pt = np.array([curr_row.get(f'{base}_x'), curr_row.get(f'{base}_y')])
            
            
            if pd.notna(prev_pt).all() and pd.notna(curr_pt).all():
                dist = np.linalg.norm(curr_pt - prev_pt)
                displacements.append(dist)
        
        if displacements and np.max(displacements) > threshold:
            events.append(CheatEvent(
                frame_index=int(curr_row['frame_index']),
                event_type="pose_jump",
                description=f"Unnatural landmark jump detected (max displacement: {np.max(displacements):.3f} normalized units).",
                severity=0.7
            ))
            
    return events

def run_all_checks(video_path: str, frame_data: pd.DataFrame, overall_threshold: int = 10) -> CheatingReport:

    all_events = []
    
    print("Running cheat detection checks...")
    
    # Run frame-based checks
    all_events.extend(detect_scene_changes(video_path))
    
    # Run data-based checks
    if not frame_data.empty:
        all_events.extend(detect_pose_jumps(frame_data))
    
    total_inconsistencies = len(all_events)
    tampering_suspected = total_inconsistencies > overall_threshold
    
    print(f"Cheat detection complete. Found {total_inconsistencies} potential inconsistencies.")
    
    return CheatingReport(
        tampering_suspected=tampering_suspected,
        total_inconsistencies=total_inconsistencies,
        events=all_events
    )
