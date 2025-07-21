import pyperclip
import time

def clipboard_watcher(callback, poll_interval=0.5):
    seen = set()
    while True:
        try:
            text = pyperclip.paste()
            if text and text not in seen:
                seen.add(text)
                callback(text)
        except Exception as e:
            print("Clipboard Error:", e)
        time.sleep(poll_interval)
