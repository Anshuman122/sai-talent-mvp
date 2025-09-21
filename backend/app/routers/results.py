from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas

from common.types import ResultRecord

router = APIRouter(
    prefix="/api/v1/results",
    tags=["Results"]
)

@router.get("/", response_model=List[schemas.Result])
def get_all_results(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):

    results = db.query(models.Result).offset(skip).limit(limit).all()

    formatted_results = []
    for db_result in results:
        test_result_obj = {
            "api_version": "v1",
            "test_name": db_result.test_name,
            "athlete_id": db_result.athlete_id,
            "timestamp": db_result.created_at.isoformat(),
            "metrics": db_result.metrics,
            "valid": db_result.is_valid,
            "confidence": db_result.confidence,
            "cheat_flags": db_result.cheat_flags
        }
        formatted_results.append({
            "id": db_result.id,
            "athlete_id": db_result.athlete_id,
            "test_result": test_result_obj,
            "created_at": db_result.created_at
        })

    return formatted_results



@router.get("/{athlete_id}", response_model=schemas.Athlete)
def get_athlete_results(athlete_id: str, db: Session = Depends(database.get_db)):

    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with id '{athlete_id}' not found."
        )


    formatted_athlete_results = []
    for db_result in athlete.results:
        test_result_obj = {
            "api_version": "v1",
            "test_name": db_result.test_name,
            "athlete_id": db_result.athlete_id,
            "timestamp": db_result.created_at.isoformat(),
            "metrics": db_result.metrics,
            "valid": db_result.is_valid,
            "confidence": db_result.confidence,
            "cheat_flags": db_result.cheat_flags
        }
        formatted_athlete_results.append({
            "id": db_result.id,
            "athlete_id": db_result.athlete_id,
            "test_result": test_result_obj,
            "created_at": db_result.created_at
        })
    

    response_data = {
        "id": athlete.id,
        "full_name": athlete.full_name,
        "email": athlete.email,
        "age": athlete.age,
        "gender": athlete.gender,
        "created_at": athlete.created_at,
        "results": formatted_athlete_results
    }
    
    return response_data

