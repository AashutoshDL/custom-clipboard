import json
import os

CLIPBOARD_FILE = "clipboard.json"
PINNED_FILE = "pinned.json"

def load_clips():
    if os.path.exists(CLIPBOARD_FILE):
        with open(CLIPBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_clips(data):
    with open(CLIPBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_pins():
    if os.path.exists(PINNED_FILE):
        with open(PINNED_FILE, "r") as f:
            return json.load(f)
    return []

def save_pins(data):
    with open(PINNED_FILE, "w") as f:
        json.dump(data, f, indent=2)
