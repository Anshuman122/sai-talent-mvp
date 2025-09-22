from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..services.processing import run_analysis_on_video
import shutil
from pathlib import Path

router = APIRouter()


UPLOAD_DIR = Path("uploaded_videos")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/", status_code=202)
def upload_video_for_analysis(
    background_tasks: BackgroundTasks,
    athlete_id: int = Form(...),
    test_name: str = Form(...),
    video_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found.")

   
    file_extension = Path(video_file.filename).suffix
    unique_filename = f"{athlete_id}_{test_name}_{Path(video_file.filename).stem}_{Path.cwd().name}{file_extension}"
    file_location = UPLOAD_DIR / unique_filename

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(video_file.file, file_object)
    finally:
        video_file.file.close()


    background_tasks.add_task(
        run_analysis_on_video,
        db_session_factory=db.session_factory, 
        video_path=str(file_location), 
        athlete_id=athlete_id, 
        test_name=test_name
    )

    return {"message": "Video accepted. Analysis is in progress.", "file_path": str(file_location)}