import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QSpacerItem, QFileDialog, QLabel, QGridLayout, QSizePolicy, QVBoxLayout, QProgressBar, QLineEdit, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from src.main import Main
from src.init import createNotebook, createVault
from src.config import NOTES_PATH, OBSIDIAN_VAULT

svg_path = 'data/svg/'

# TODO get this progress bar to update dynamically with the yields
# TODO be able to reset the window after pdfs have been loaded
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
        self.selected_files = []

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
        self.selected_files = files
        self.fileName = files_formatted

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
        self.selected_files = files
        self.fileName = files_formatted

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rivet")
        self.setGeometry(100, 100, 730, 600)

        # Layout and Widgets
        self.layOut = QGridLayout(self)

        self.label = QLabel("Select a vault")
        self.button = QPushButton("Select Obsidian Vault")
        self.dropbox = QScrollArea()
        self.dropboxTemp = DropBox()
        self.dropbox.setWidget(self.dropboxTemp)
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
        self.notebook = QLineEdit("", placeholderText="Enter notebook name")

        self.button.clicked.connect(self.select_folder)
        self.load.clicked.connect(self.load_files)

        self.layOut.addWidget(self.label, 0, 0)
        self.layOut.addWidget(self.button, 1, 0)
        self.layOut.addWidget(self.notebook, 2, 0)
        self.layOut.addWidget(self.dropbox, 3, 0)
        self.layOut.addWidget(self.refMarkerStart, 4, 0)
        self.layOut.addWidget(self.refMarkerEnd, 5, 0)
        self.layOut.addWidget(self.load, 6, 0)

        # Add vertical spacers between the rows
        self.layOut.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0)  # Spacer between row 1 and 2

        self.setLayout(self.layOut)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.label.setText(f"Selected: {folder}")
        print(folder)
    
    # Add alerts if things aren't filled out
    def load_files(self):
        # Getting data
        notebook = self.notebook.text()
        refMarker = (self.refMarkerStart.text(), self.refMarkerEnd.text())
        createVault(OBSIDIAN_VAULT) # Change to selected vault TODO
        createNotebook(OBSIDIAN_VAULT, notebook)

        # Copy selected files to NOTES_PATH
        self.selected_files = self.dropboxTemp.selected_files
        self.fileNames = self.dropboxTemp.fileName
        for i, file in enumerate(self.selected_files):
            with open(file, 'rb') as file:
                data = file.read()
                if self.fileNames[i] not in os.listdir(NOTES_PATH+notebook):
                    with open(NOTES_PATH+notebook+"/"+f"{self.fileNames[i]}", 'wb') as file:
                        file.write(data)

        # Starting the progress bar
        self.layOut.addWidget(self.progressBar, 7, 0)
        total_progress = len(os.listdir(NOTES_PATH))*2
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(total_progress)
        self.progressBar.setValue(0)

        # Initialize main function
        main = Main()
        load_generator = main.load(notebook)
        for index in load_generator:
            self.progressBar.setValue(index)
        write_generator = main.write(refMarker, notebook)
        for index in write_generator:
            index += total_progress/2 # So the progress bar doesn't reset
            self.progressBar.setValue(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
