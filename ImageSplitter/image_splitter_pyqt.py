import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QSpinBox)
from PIL import Image

class ImageSplitter(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Grid Splitter")
        self.init_ui()

    def init_ui(self):  
        layout = QVBoxLayout()  

        # Pulsante seleziona immagine  
        self.btn_file = QPushButton("Seleziona immagine")  
        self.btn_file.clicked.connect(self.select_file)  
        self.label_file = QLabel("Nessun file selezionato")  

        # Input righe e colonne  
        row_layout = QHBoxLayout()  
        row_layout.addWidget(QLabel("Righe:"))  
        self.spin_rows = QSpinBox()  
        self.spin_rows.setMinimum(1)  
        self.spin_rows.setValue(4)  
        row_layout.addWidget(self.spin_rows)  

        col_layout = QHBoxLayout()  
        col_layout.addWidget(QLabel("Colonne:"))  
        self.spin_cols = QSpinBox()  
        self.spin_cols.setMinimum(1)  
        self.spin_cols.setValue(4)  
        col_layout.addWidget(self.spin_cols)  

        # Pulsante seleziona cartella output  
        self.btn_folder = QPushButton("Seleziona cartella di destinazione")  
        self.btn_folder.clicked.connect(self.select_folder)  
        self.label_folder = QLabel("Nessuna cartella selezionata")  

        # Pulsante esegui  
        self.btn_split = QPushButton("Dividi immagine")  
        self.btn_split.clicked.connect(self.split_image)  

        # Aggiungi widget al layout  
        layout.addWidget(self.btn_file)  
        layout.addWidget(self.label_file)  
        layout.addLayout(row_layout)  
        layout.addLayout(col_layout)  
        layout.addWidget(self.btn_folder)  
        layout.addWidget(self.label_folder)  
        layout.addWidget(self.btn_split)  

        self.setLayout(layout)  
        self.file_path = None  
        self.output_dir = None  

    def select_file(self):  
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona immagine", "", "Image files (*.jpg *.jpeg *.png *.bmp)")  
        if file_path:  
            self.file_path = file_path  
            self.label_file.setText(file_path)  

    def select_folder(self):  
        folder = QFileDialog.getExistingDirectory(self, "Seleziona cartella di destinazione")  
        if folder:  
            self.output_dir = folder  
            self.label_folder.setText(folder)  

    def split_image(self):  
        if not self.file_path or not self.output_dir:  
            QMessageBox.warning(self, "Attenzione", "Seleziona immagine e cartella di destinazione")  
            return  

        rows = self.spin_rows.value()  
        cols = self.spin_cols.value()  

        img = Image.open(self.file_path)  
        width, height = img.size  
        w = width // cols  
        h = height // rows  

        count = 1  
        for i in range(rows):  
            for j in range(cols):  
                box = (j*w, i*h, (j+1)*w, (i+1)*h)  
                cell = img.crop(box)  
                cell.save(os.path.join(self.output_dir, f"foto_{count}.png"))  
                count += 1  

        QMessageBox.information(self, "Completato", f"{count-1} immagini salvate in {self.output_dir}")  

if __name__ == "**main**":
    app = QApplication(sys.argv)
    splitter = ImageSplitter()
    splitter.show()
    sys.exit(app.exec())
