from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import numpy as np


class FITSView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Configuration de l'interface
        self.setWindowTitle("Application FITS - MVC")
        self.layout = QVBoxLayout(self)

        # Boutons
        self.load_button = QPushButton("Charger 3 fichiers FIT")
        self.load_button.clicked.connect(self.controller.load_fit_files)

        self.show_button = QPushButton("Afficher l'image")
        self.show_button.clicked.connect(self.controller.display_image)
        self.show_button.setEnabled(False)

        # Label pour afficher l'image
        self.image_label = QLabel("L'image sera affichée ici.")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajout des widgets
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.show_button)
        self.layout.addWidget(self.image_label)

    def open_file_dialog(self):
        """Ouvre un dialogue pour sélectionner 3 fichiers FIT."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez 3 fichiers FIT", "", "Fichiers FIT (*.fit)"
        )
        return files, _

    def set_image(self, rgb_image: np.ndarray):
        """Affiche l'image dans le QLabel."""
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            (rgb_image * 255).astype(np.uint8), width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)