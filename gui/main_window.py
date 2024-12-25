import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
import keybinder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kranky-binder")
        self.resize(600, 400)

        # Main widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Layout
        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)

        # Table for showing existing keybinds
        self.table = QTableWidget(0, 3)  # columns: Hotkey, Text, Enabled
        self.table.setHorizontalHeaderLabels(["Hotkey", "Text", "Enabled"])
        self.layout.addWidget(self.table)

        # Section for adding new keybind
        form_layout = QHBoxLayout()

        # Hotkey Combo
        self.hotkey_combo = QComboBox()
        # Populate with possible keys:
        # TODO detect hotkey onpress
        common_keys = ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
                       "1","2","3","4","5","6","7","8","9","0",
                       "a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                       "o","p","q","r","s","t","u","v","w","x","y","z"]
        for k in common_keys:
            self.hotkey_combo.addItem(k)
        
        form_layout.addWidget(QLabel("Hotkey:"))
        form_layout.addWidget(self.hotkey_combo)

        # Text field
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Enter the text to send...")
        form_layout.addWidget(self.text_edit)

        # Add button
        self.add_button = QPushButton("Add Keybind")
        self.add_button.clicked.connect(self.add_keybind)
        form_layout.addWidget(self.add_button)

        self.layout.addLayout(form_layout)

        # Save button (optional)
        self.save_button = QPushButton("Save Keybinds")
        self.save_button.clicked.connect(self.save_keybinds_to_config)
        self.layout.addWidget(self.save_button)

        # Load button (optional)
        self.load_button = QPushButton("Load Keybinds")
        self.load_button.clicked.connect(lambda: self.load_keybinds_from_config("config.json"))
        self.layout.addWidget(self.load_button)

        self.keybinds = []

    def add_keybind(self):
        hotkey = self.hotkey_combo.currentText()
        text = self.text_edit.text()

        if not hotkey or not text:
            return  # or show error message

        new_bind = {
            "key": hotkey,
            "text": text,
            "enabled": True
        }
        self.keybinds.append(new_bind)

        # Update table
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        self.table.setItem(row_idx, 0, QTableWidgetItem(hotkey))
        self.table.setItem(row_idx, 1, QTableWidgetItem(text))
        self.table.setItem(row_idx, 2, QTableWidgetItem("True"))

        self.text_edit.clear()

        # Update the global keybind list in keybinder
        keybinder.set_keybinds(self.keybinds)

    def save_keybinds_to_config(self):
        # Build list from table or use self.keybinds
        with open("config.json", "w") as f:
            json.dump({"keybinds": self.keybinds}, f, indent=2)

    def load_keybinds_from_config(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.keybinds = data.get("keybinds", [])
        except FileNotFoundError:
            self.keybinds = []

        # Clear table
        self.table.setRowCount(0)

        # Populate table
        for bind in self.keybinds:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)

            self.table.setItem(row_idx, 0, QTableWidgetItem(bind["key"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(bind["text"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(bind["enabled"])))

        # Update the global keybind list in keybinder
        keybinder.set_keybinds(self.keybinds)
