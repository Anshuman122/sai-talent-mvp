import argparse
import json
from pathlib import Path
from typing import Optional

CONFIG_FILE = Path(__file__).resolve().parent.parent / 'manual_test_results.json'

def save_sit_and_reach(reach_cm: float):
    """Saves the user's sit and reach result to the shared config file."""
    data = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass  
    
    data['sit_and_reach_cm'] = reach_cm
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Sit and Reach result saved as {reach_cm} cm in '{CONFIG_FILE}'.")

def get_sit_and_reach() -> Optional[float]:
    """Retrieves the user's sit and reach result from the shared config file."""
    if not CONFIG_FILE.exists():
        return None
        
    with open(CONFIG_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data.get('sit_and_reach_cm')
        except json.JSONDecodeError:
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set and save the sit and reach result in centimeters.")
    parser.add_argument(
        "value",
        type=float,
        help="The result in centimeters (e.g., 15.0)."
    )
    
    args = parser.parse_args()
    save_sit_and_reach(args.value)

