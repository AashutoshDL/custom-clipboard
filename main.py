import threading
import pyperclip
from PyQt5.QtWidgets import QApplication
from gui import ClipStackGUI
from clipboard import clipboard_watcher
from storage import load_clips, save_clips, load_pins, save_pins

history = []
pins = []

def on_new_clip(text):
    print("📋 Copied:", text)
    history.append(text)
    gui.add_clip(text)
    save_clips(history)

def on_select_clip(text):
    pyperclip.copy(text)

if __name__ == "__main__":
    history = load_clips()
    pins = load_pins()

    app = QApplication([])
    gui = ClipStackGUI(on_select_clip=on_select_clip)

    gui.load_initial_pins(pins)
    gui.load_initial_clips(history)

    watcher_thread = threading.Thread(target=clipboard_watcher, args=(on_new_clip,), daemon=True)
    watcher_thread.start()

    gui.show()
    app.exec_()

    # Save on exit
    pins = [gui.pinned_list.item(i).text() for i in range(gui.pinned_list.count())]
    history = [gui.clip_list.item(i).text() for i in range(gui.clip_list.count())]

    save_pins(pins)
    save_clips(history)
