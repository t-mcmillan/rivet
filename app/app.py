import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QSpacerItem, QFileDialog, QLabel, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter

class DropLabel(QLabel):
    def __init__(self):
        super().__init__("Click to select files or drag and drop them")
        #self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1.5px dashed #aaa; padding: 10px;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        files_formatted = [file.split("/")[-1] for file in files]
        self.setText("\n".join(files_formatted))
        if files == []:
            self.setText("Click to select files or drag and drop them")

    def mousePressEvent(self, event):
        # Check if the event is a left mouse click
        if event.button() == Qt.LeftButton:
            # Open file dialog to choose a file
            files, _ = QFileDialog.getOpenFileNames(self)
            files_formatted = [file.split("/")[-1] for file in files]
            self.setText("\n".join(files_formatted))
        if files == []:
            self.setText("Click to select files or drag and drop them")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rivet")
        self.setGeometry(100, 100, 300, 200)

        # Layout and Widgets
        layout = QGridLayout(self)

        self.label = QLabel("Select a vault")
        self.button = QPushButton("Select Obsidian Vault")
        self.dropbox = DropLabel()

        self.button.clicked.connect(self.select_folder)

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.button, 1, 0)
        layout.addWidget(self.dropbox, 2, 0)

        # Add vertical spacers between the rows
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0)  # Spacer between row 1 and 2

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.label.setText(f"Selected: {folder}")
        print(folder)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
