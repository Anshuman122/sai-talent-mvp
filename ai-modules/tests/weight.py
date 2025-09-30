import argparse
import json
from pathlib import Path
from typing import Optional

CONFIG_FILE = Path(__file__).resolve().parent.parent / 'manual_test_results.json'

def save_weight(weight_kg: float):
    """Saves the user's weight to the shared config file."""
    data = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    
    data['weight_kg'] = weight_kg
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Weight saved as {weight_kg} kg in '{CONFIG_FILE}'.")

def get_weight() -> Optional[float]:
    """Retrieves the user's weight from the shared config file."""
    if not CONFIG_FILE.exists():
        return None
        
    with open(CONFIG_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data.get('weight_kg')
        except json.JSONDecodeError:
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set and save the user's weight in kilograms.")
    parser.add_argument(
        "value",
        type=float,
        help="The user's weight in kilograms (e.g., 72.0)."
    )
    
    args = parser.parse_args()
    save_weight(args.value)

