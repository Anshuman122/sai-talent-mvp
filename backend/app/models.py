from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    
    results = relationship("TestResult", back_populates="athlete")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"))
    test_name = Column(String, index=True)
    video_path = Column(String)
    results_data = Column(JSON) 
    cheating_report = Column(JSON) 
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    athlete = relationship("Athlete", back_populates="results")
