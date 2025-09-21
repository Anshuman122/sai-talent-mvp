from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

from common.types import TestResult, ResultRecord

class ResultCreate(BaseModel):
    test_name: str
    athlete_id: str
    metrics: dict
    is_valid: bool
    confidence: float
    cheat_flags: dict

class Result(BaseModel):
    id: int
    athlete_id: str
    test_result: TestResult
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)



class AthleteCreate(BaseModel):
    full_name: str
    email: str
    age: int
    gender: str

class Athlete(BaseModel):
    id: str
    full_name: str
    email: str
    age: int
    gender: str
    created_at: datetime
    results: List[Result] = [] 

    model_config = ConfigDict(from_attributes=True)
