import pyperclip
import time
import hashlib

def clipboard_watcher(callback, 
                     min_interval=0.5,    # Faster for responsiveness
                     max_interval=2.0,    # Reduced max interval  
                     idle_threshold=5     # Reduced idle threshold
                     ):
    last_hash = None
    poll_interval = min_interval
    last_change_time = time.time()
    
    while True:
        try:
            text = pyperclip.paste()
            if text:  # Only process non-empty text
                # Use hash for efficient comparison
                current_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                
                if current_hash != last_hash:
                    last_hash = current_hash
                    callback(text)
                    poll_interval = min_interval
                    last_change_time = time.time()
                else:
                    # Adaptive polling
                    idle_time = time.time() - last_change_time
                    if idle_time > idle_threshold:
                        poll_interval = min(poll_interval * 1.2, max_interval)
                        
        except Exception as e:
            print(f"Clipboard Error: {e}")
            
        time.sleep(poll_interval)