import json
import os
from pathlib import Path

# Use user data directory
DATA_DIR = Path.home() / '.clipboard_manager'
DATA_DIR.mkdir(exist_ok=True)

CLIPBOARD_FILE = DATA_DIR / "clipboard.json"
PINNED_FILE = DATA_DIR / "pinned.json"

def load_clips():
    try:
        if CLIPBOARD_FILE.exists():
            with open(CLIPBOARD_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                return data[:100]  # Limit loaded items
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading clips: {e}")
    return []

def save_clips(data):
    try:
        # Limit saved data
        limited_data = data[:100] if len(data) > 100 else data
        with open(CLIPBOARD_FILE, "w", encoding='utf-8') as f:
            json.dump(limited_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error saving clips: {e}")

def load_pins():
    try:
        if PINNED_FILE.exists():
            with open(PINNED_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading pins: {e}")
    return []

def save_pins(data):
    try:
        with open(PINNED_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error saving pins: {e}")