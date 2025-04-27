import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QSpacerItem, QFileDialog, QLabel, QGridLayout, QSizePolicy, QVBoxLayout, QProgressBar, QLineEdit, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from src.main import Main

svg_path = 'data/svg/'

def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())     

class IconLabel(QWidget):
    def __init__(self, file: str):
        super().__init__()
        layout = QVBoxLayout(self)
        if file.split(".")[1]+".svg" in os.listdir(svg_path):
            svg_widget = QSvgWidget(f"{svg_path}{file.split(".")[1]}.svg")
        else:
            svg_widget = QSvgWidget(f"{svg_path}no-format.svg")
        svg_widget.setFixedSize(40, 40)
        layout.addWidget(svg_widget, alignment=Qt.AlignCenter)
        if len(file) > 15:
            file = file[0:12]+"..."
        layout.addWidget(QLabel(file), alignment=Qt.AlignTop | Qt.AlignHCenter)

class DropBox(QWidget):
    def __init__(self):
        super().__init__()
        #self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("padding: 15px;")
        self.setAcceptDrops(True)
        self.layOut = QGridLayout(self)
        self.label = QLabel("Click to select files or drag and drop them")
        self.layOut.addWidget(self.label, 0, 0, alignment=Qt.AlignCenter)
        self.layOut.setVerticalSpacing(20)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        files_formatted: list[str] = [file.split("/")[-1] for file in files]
        clearLayout(self.layOut)
        row = 0
        for index, file in enumerate(files_formatted):
            self.layOut.addWidget(IconLabel(file), row, index%4)
            if index%4 == 3:
                row += 1
        if files == []:
            self.layOut.addWidget(QLabel("Click to select files or drag and drop them"), 0, 0, alignment=Qt.AlignCenter)

    def mousePressEvent(self, event):
        # Check if the event is a left mouse click
        if event.button() == Qt.LeftButton:
            # Open file dialog to choose a file
            files, _ = QFileDialog.getOpenFileNames(self)
            files_formatted = [file.split("/")[-1] for file in files]
            clearLayout(self.layOut)
            row = 0
            for index, file in enumerate(files_formatted):
                self.layOut.addWidget(IconLabel(file), row, index%4)
                if index%4 == 3:
                    row += 1
        if files == []:
            self.layOut.addWidget(QLabel("Click to select files or drag and drop them"), 0, 0, alignment=Qt.AlignCenter)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rivet")
        self.setGeometry(100, 100, 700, 600)

        # Layout and Widgets
        layout = QGridLayout(self)

        self.label = QLabel("Select a vault")
        self.button = QPushButton("Select Obsidian Vault")
        self.dropbox = QScrollArea()
        self.dropbox.setWidget(DropBox())
        self.dropbox.setWidgetResizable(True)
        self.load = QPushButton("Go!")
        self.progressBar = QProgressBar()
        # Set background color and text color
        self.load.setStyleSheet("""
            QPushButton {
                background-color: #3498db;  /* blue background */
                color: white;               /* white text */
                border-radius: 10px;         /* rounded corners */
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;  /* darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #1c5980;  /* even darker when pressed */
            }
        """)
        self.refMarkerStart = QLineEdit("", placeholderText="Enter start reference marker")
        self.refMarkerEnd = QLineEdit("", placeholderText="Enter end reference marker")

        self.button.clicked.connect(self.select_folder)
        self.load.clicked.connect(self.load_files)
        print(self.refMarkerStart.text())

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.button, 1, 0)
        layout.addWidget(self.dropbox, 2, 0)
        layout.addWidget(self.refMarkerStart, 3, 0)
        layout.addWidget(self.refMarkerEnd, 4, 0)
        layout.addWidget(self.load, 5, 0)
        layout.addWidget(self.progressBar, 6, 0)

        # Add vertical spacers between the rows
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0)  # Spacer between row 1 and 2

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.label.setText(f"Selected: {folder}")
        print(folder)
    
    def load_files(self):
        pass 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
