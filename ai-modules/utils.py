import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple, Optional, List, Dict
from pathlib import Path


from .base import VideoProperties

AI_MODULES_ROOT = Path(__file__).resolve().parent

def load_video_properties(video_path: str) -> Tuple[Optional[cv2.VideoCapture], Optional[VideoProperties]]:

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return None, None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    properties = VideoProperties(
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        fps=fps,
        frame_count=frame_count,
        duration_seconds=frame_count / fps if fps > 0 else 0
    )
    return cap, properties

def initialize_pose_model(static_mode: bool = False, complexity: int = 1, min_det_conf: float = 0.5, min_track_conf: float = 0.5) -> mp.solutions.pose.Pose:
    """Initializes and returns a MediaPipe Pose model with specified parameters."""
    return mp.solutions.pose.Pose(
        static_image_mode=static_mode,
        model_complexity=complexity,
        min_detection_confidence=min_det_conf,
        min_tracking_confidence=min_track_conf
    )

def create_video_writer(output_path: str, fps: float, width: int, height: int) -> Optional[cv2.VideoWriter]:
    """Creates and returns a cv2.VideoWriter object for saving annotated videos."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        print(f"Error: Could not initialize VideoWriter for path {output_path}")
        return None
    return out

def extract_landmarks(results: any, landmark_enums: List) -> Optional[Dict[str, np.ndarray]]:

    if not results.pose_landmarks:
        return None

    landmarks = {}
    for lm_enum in landmark_enums:
        lm = results.pose_landmarks.landmark[lm_enum.value]
        landmarks[lm_enum.name] = np.array([lm.x, lm.y, lm.z, lm.visibility])
    return landmarks
