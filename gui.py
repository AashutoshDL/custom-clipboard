from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
import pyperclip
from storage import save_clips, save_pins

class ClipStackGUI(QWidget):
    def __init__(self, on_select_clip=None):
        super().__init__()
        self.setWindowTitle("ClipStack 🔥")
        self.setFixedSize(500, 600)

        self.layout = QVBoxLayout()

        # Labels
        self.label_pinned = QLabel("📌 Pinned Clips")
        self.label_history = QLabel("📋 Clipboard History")

        # Lists
        self.pinned_list = QListWidget()
        self.clip_list = QListWidget()

        # Buttons
        self.copy_button = QPushButton("Copy Selected")
        self.pin_button = QPushButton("📌 Pin Selected")
        self.clear_button = QPushButton("🧹 Clear Clipboard History")

        # Add widgets to layout
        self.layout.addWidget(self.label_pinned)
        self.layout.addWidget(self.pinned_list)
        self.layout.addWidget(self.label_history)
        self.layout.addWidget(self.clip_list)
        self.layout.addWidget(self.copy_button)
        self.layout.addWidget(self.pin_button)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)

        # Connect buttons
        self.copy_button.clicked.connect(self.copy_selected)
        self.pin_button.clicked.connect(self.pin_selected)
        self.clear_button.clicked.connect(self.clear_clips)

        self.on_select_clip = on_select_clip

    def add_clip(self, clip):
        # Avoid duplicates in history and pinned
        if self.clip_list.findItems(clip, Qt.MatchExactly):
            return
        if self.pinned_list.findItems(clip, Qt.MatchExactly):
            return
        self.clip_list.insertItem(0, clip)

    def add_pin(self, clip):
        if not self.pinned_list.findItems(clip, Qt.MatchExactly):
            self.pinned_list.insertItem(0, clip)

    def load_initial_clips(self, clips):
        for clip in reversed(clips):
            self.add_clip(clip)

    def load_initial_pins(self, pins):
        for pin in reversed(pins):
            self.add_pin(pin)

    def copy_selected(self):
        # Check pinned list first
        item = self.pinned_list.currentItem() or self.clip_list.currentItem()
        if item and self.on_select_clip:
            self.on_select_clip(item.text())

    def pin_selected(self):
        item = self.clip_list.currentItem()
        if item:
            clip_text = item.text()
            self.add_pin(clip_text)
            # Remove from history list
            self.clip_list.takeItem(self.clip_list.row(item))
            # Save pins immediately
            pins = [self.pinned_list.item(i).text() for i in range(self.pinned_list.count())]
            save_pins(pins)

            # Save updated history
            history = [self.clip_list.item(i).text() for i in range(self.clip_list.count())]
            save_clips(history)

    def clear_clips(self):
        reply = QMessageBox.question(
            self, 'Clear History?', 'Are you sure you want to clear all clipboard history? (Pinned clips will stay)',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clip_list.clear()
            save_clips([])

