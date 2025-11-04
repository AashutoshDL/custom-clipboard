#!/usr/bin/env python3
# main.py
import threading
import pyperclip
from PyQt5.QtWidgets import QApplication # type: ignore
from .gui import ClipStackGUI
from .clipboard import clipboard_watcher
from .storage import load_clips, save_clips, load_pins, save_pins

class ClipboardManager:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.history = load_clips()
        self.pins = load_pins()
        self.gui = None
        self._save_pending = False
        
    def on_new_clip(self, text):
        # Prevent duplicate entries at the top
        if self.history and self.history[0] == text:
            return
            
        # Remove if exists elsewhere in history
        if text in self.history:
            self.history.remove(text)
            
        # Add to front and limit size
        self.history.insert(0, text)
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        if self.gui:
            self.gui.add_clip(text)
        
        # Batch save to reduce I/O
        self._schedule_save()
    
    def on_select_clip(self, text):
        pyperclip.copy(text)
        
    def _schedule_save(self):
        if not self._save_pending:
            self._save_pending = True
            # Save after 2 seconds of inactivity
            threading.Timer(2.0, self._save_data).start()
    
    def _save_data(self):
        save_clips(self.history)
        self._save_pending = False
    
    def save_on_exit(self):
        # Get current state from GUI
        if self.gui:
            self.pins = [self.gui.pinned_list.item(i).text() 
                        for i in range(self.gui.pinned_list.count())]
            self.history = [self.gui.clip_list.item(i).text() 
                           for i in range(self.gui.clip_list.count())]
        
        save_pins(self.pins)
        save_clips(self.history)

def main():
    manager = ClipboardManager()
    
    app = QApplication([])
    gui = ClipStackGUI(
        on_select_clip=manager.on_select_clip,
        manager=manager  # Pass manager reference
    )
    manager.gui = gui
    
    gui.load_initial_pins(manager.pins)
    gui.load_initial_clips(manager.history)
    
    watcher_thread = threading.Thread(
        target=clipboard_watcher, 
        args=(manager.on_new_clip,), 
        daemon=True
    )
    watcher_thread.start()
    
    gui.show()
    app.exec_()
    
    manager.save_on_exit()
    
# Allow running directly for development
if __name__ == "__main__":
    main()
