import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker

AI_MODULES_PATH = str(Path(__file__).resolve().parents[2] / 'ai-modules')
if AI_MODULES_PATH not in sys.path:
    sys.path.append(AI_MODULES_PATH)


from tests.situps import analyze_situps
from tests.vertical_jump import analyze_vertical_jump
from tests.broad_jump import analyze_broad_jump
from tests.sprint_30m import analyze_sprint_30m
from tests.shuttle_run import analyze_shuttle_run
from tests.endurance_run import analyze_endurance_run
from tests.medicine_ball import analyze_medicine_ball_throw

from .. import models
from ..database import SessionLocal



ANALYSIS_FUNCTION_MAP = {
    "situps": analyze_situps,
    "vertical_jump": analyze_vertical_jump,
    "broad_jump": analyze_broad_jump,
    "sprint_30m": analyze_sprint_30m,
    "shuttle_run": analyze_shuttle_run,
    "endurance_run": analyze_endurance_run,
    "medicine_ball": analyze_medicine_ball_throw
}

def run_analysis_on_video(db_session_factory: sessionmaker, video_path: str, athlete_id: int, test_name: str):

    print(f"Starting analysis for test '{test_name}' on video: {video_path}")
    

    analysis_function = ANALYSIS_FUNCTION_MAP.get(test_name)
    if not analysis_function:
        print(f"Error: No analysis function found for test '{test_name}'")
        return


    db = db_session_factory()
    try:
        
        ai_result = analysis_function(video_path)
        
        
        new_result = models.TestResult(
            athlete_id=athlete_id,
            test_name=test_name,
            video_path=video_path,
            results_data=ai_result.results,
            cheating_report=ai_result.cheating_report.model_dump()
        )
        db.add(new_result)
        db.commit()
        print(f"Successfully saved results for test '{test_name}' for athlete {athlete_id}.")

    except Exception as e:
        print(f"🔴 AI analysis failed for video {video_path}. Error: {e}")
        
    finally:
        db.close()
