from PyQt5.QtWidgets import ( #type: ignore
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QPushButton, QMessageBox, QLabel, QSplitter
)
from PyQt5.QtCore import Qt, QTimer #type: ignore
import pyperclip
from .storage import save_clips, save_pins

class ClipStackGUI(QWidget):
    def __init__(self, on_select_clip=None, manager=None):
        super().__init__()
        self.manager = manager
        self.setWindowTitle("Clipboard Manager")
        self.setGeometry(100, 100, 600, 700)
        
        self.init_ui()
        self.on_select_clip = on_select_clip
        
        # Debounce timer for saves
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._save_state)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Use splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        
        # Pinned section
        pinned_widget = QWidget()
        pinned_layout = QVBoxLayout(pinned_widget)
        pinned_layout.addWidget(QLabel("📌 Pinned Clips"))
        
        self.pinned_list = QListWidget()
        self.pinned_list.setMaximumHeight(150)  # Limit height
        pinned_layout.addWidget(self.pinned_list)
        
        # History section  
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.addWidget(QLabel("📋 Clipboard History"))
        
        self.clip_list = QListWidget()
        history_layout.addWidget(self.clip_list)
        
        splitter.addWidget(pinned_widget)
        splitter.addWidget(history_widget)
        splitter.setStretchFactor(1, 1)  # History takes more space
        
        layout.addWidget(splitter)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton("📋 Copy")
        self.pin_button = QPushButton("📌 Pin")
        self.unpin_button = QPushButton("📌❌ Unpin")
        self.clear_button = QPushButton("🗑️ Clear History")
        
        # Make buttons more compact
        for btn in [self.copy_button, self.pin_button, self.unpin_button, self.clear_button]:
            btn.setMaximumHeight(30)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.pin_button)
        button_layout.addWidget(self.unpin_button)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect signals
        self.copy_button.clicked.connect(self.copy_selected)
        self.pin_button.clicked.connect(self.pin_selected)
        self.unpin_button.clicked.connect(self.unpin_selected)
        self.clear_button.clicked.connect(self.clear_clips)
        
        # Double-click to copy
        self.pinned_list.itemDoubleClicked.connect(lambda item: self.on_select_clip(item.text()))
        self.clip_list.itemDoubleClicked.connect(lambda item: self.on_select_clip(item.text()))
    
    def add_clip(self, clip):
        # More efficient duplicate checking
        for i in range(self.clip_list.count()):
            if self.clip_list.item(i).text() == clip:
                return
                
        # Check if already pinned
        for i in range(self.pinned_list.count()):
            if self.pinned_list.item(i).text() == clip:
                return
                
        self.clip_list.insertItem(0, clip)
        
        # Limit display items for performance
        if self.clip_list.count() > 100:
            self.clip_list.takeItem(self.clip_list.count() - 1)
    
    def add_pin(self, clip):
        # Check for duplicates
        for i in range(self.pinned_list.count()):
            if self.pinned_list.item(i).text() == clip:
                return
        self.pinned_list.insertItem(0, clip)
    
    def load_initial_clips(self, clips):
        self.clip_list.clear()
        for clip in clips:
            self.clip_list.addItem(clip)
    
    def load_initial_pins(self, pins):
        self.pinned_list.clear()
        for pin in pins:
            self.pinned_list.addItem(pin)
    
    def copy_selected(self):
        item = self.pinned_list.currentItem() or self.clip_list.currentItem()
        if item and self.on_select_clip:
            self.on_select_clip(item.text())
    
    def pin_selected(self):
        item = self.clip_list.currentItem()
        if not item:
            return
            
        clip_text = item.text()
        self.add_pin(clip_text)
        self.clip_list.takeItem(self.clip_list.row(item))
        
        self._schedule_save()
    
    def unpin_selected(self):
        item = self.pinned_list.currentItem()
        if not item:
            return
            
        clip_text = item.text()
        self.pinned_list.takeItem(self.pinned_list.row(item))
        self.add_clip(clip_text)
        
        self._schedule_save()
    
    def clear_clips(self):
        reply = QMessageBox.question(
            self, 'Clear History?', 
            'Clear all clipboard history? (Pinned clips remain)',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.clip_list.clear()
            if self.manager:
                self.manager.history.clear()
            save_clips([])
    
    def _schedule_save(self):
        # Debounce saves
        self.save_timer.start(1000)  # Save after 1 second
    
    def _save_state(self):
        pins = [self.pinned_list.item(i).text() for i in range(self.pinned_list.count())]
        history = [self.clip_list.item(i).text() for i in range(self.clip_list.count())]
        
        save_pins(pins)
        save_clips(history)
        
        # Update manager state
        if self.manager:
            self.manager.pins = pins
            self.manager.history = history