import argparse
import json
from pathlib import Path
from typing import Optional


CONFIG_FILE = Path(__file__).resolve().parent.parent / 'manual_test_results.json'

def save_height(height_cm: float):
    """Saves the user's height to the shared config file."""
    data = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass  
    
    data['height_cm'] = height_cm
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Height saved as {height_cm} cm in '{CONFIG_FILE}'.")

def get_height() -> Optional[float]:
    """Retrieves the user's height from the shared config file."""
    if not CONFIG_FILE.exists():
        return None
        
    with open(CONFIG_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data.get('height_cm')
        except json.JSONDecodeError:
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set and save the user's height in centimeters.")
    parser.add_argument(
        "value",
        type=float,
        help="The user's height in centimeters (e.g., 175.5)."
    )
    
    args = parser.parse_args()
    save_height(args.value)
