from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd

class VideoProperties(BaseModel):
    
    width: int
    height: int
    fps: float
    frame_count: int
    duration_seconds: float

class CheatEvent(BaseModel):
   
    frame_index: Optional[int] = None
    event_type: str = Field(..., description="Type of anomaly, e.g., 'pose_jump', 'scene_cut'")
    description: str
    severity: float = Field(default=0.5, description="A score from 0.0 to 1.0 indicating severity.")

class CheatingReport(BaseModel):
    
    tampering_suspected: bool = False
    total_inconsistencies: int = 0
    events: List[CheatEvent] = []

class AnalysisResult(BaseModel):

    test_name: str
    video_properties: VideoProperties
    
    results: Dict[str, Any] = Field(..., description="Key metrics for the specific test, e.g., {'situp_count': 17}")
    
    frame_data: pd.DataFrame = Field(..., description="DataFrame with frame-by-frame analysis.")
    cheating_report: CheatingReport

    class Config:
        arbitrary_types_allowed = True 