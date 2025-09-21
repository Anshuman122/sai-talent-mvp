from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd

class CheatFlags(BaseModel):
    
    manipulation_score: float = Field(0.0, ge=0.0, le=1.0, description="Overall likelihood of tampering.")
    scene_cuts_detected: List[int] = Field([], description="Frames where scene cuts were detected.")
    pose_jumps_detected: List[int] = Field([], description="Frames with unnatural pose movement.")
    low_confidence_frames: List[int] = Field([], description="Frames with low landmark confidence.")

class TestResult(BaseModel):

    api_version: str = "v1"
    test_name: str                 
    athlete_id: str             
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metrics: Dict[str, Any]    
    valid: bool              
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the accuracy of the metrics.")
    cheat_flags: CheatFlags = Field(default_factory=CheatFlags)
    raw: Optional[Dict[str, Any]] = None 

class JobStatus(BaseModel):
    
    job_id: str
    status: str 
    progress: int = Field(0, ge=0, le=100)
    result: Optional[TestResult] = None
    error_message: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ResultRecord(BaseModel):
    id: int
    result: TestResult
    stored_at: datetime

    class Config:
        from_attributes = True