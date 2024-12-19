from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSlider, QLabel, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt
import numpy as np
from ImageWidget import ImageWidget

class FITSView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Application FITS - MVC")
        self.main_layout = QHBoxLayout(self)

        self.controls_layout = QVBoxLayout()

        # Boutons et curseurs
        self.load_button = QPushButton("Charger 3 fichiers FIT")
        self.load_button.clicked.connect(self.controller.load_fit_files)
        self.load_button.setMaximumWidth(160)
        self.load_button.setMaximumHeight(30)

        self.contrast_label = QLabel("Contraste")
        self.contrast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter des espaces pour centrer verticalement
        spacer_top = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        slider_layout = QVBoxLayout()

        # Fonction pour créer un curseur vertical avec ses labels
        def create_slider(label_text):
            layout = QVBoxLayout()
            slider_label = QLabel(label_text)
            slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_top = QLabel("100")
            label_bottom = QLabel("0")
            slider = QSlider(Qt.Orientation.Vertical)

            # Ajuster la taille
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setMinimumHeight(160) 
            slider.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            slider.setMaximumWidth(20)

            # Ajout des widgets dans le layout
            layout.addWidget(slider_label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_top, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_bottom, alignment=Qt.AlignmentFlag.AlignCenter)

            return layout, slider

        # Création des curseurs rouge, vert et bleu
        red_layout, self.red_slider = create_slider("Rouge")
        green_layout, self.green_slider = create_slider("Vert")
        blue_layout, self.blue_slider = create_slider("Bleu")

        slider_layout.addLayout(red_layout)
        slider_layout.addLayout(green_layout)
        slider_layout.addLayout(blue_layout)

        self.apply_button = QPushButton("Appliquer les Changements")
        self.apply_button.clicked.connect(self.controller.apply_changes)
        self.apply_button.setMaximumWidth(160)
        self.apply_button.setMaximumHeight(30)

        self.download_button = QPushButton("Télécharger les images")
        self.download_button.setMaximumWidth(160)
        self.download_button.setMaximumHeight(30)

        # Ajout des widgets dans controls_layout
        self.controls_layout.addWidget(self.load_button)
        self.controls_layout.addSpacerItem(spacer_top)
        self.controls_layout.addWidget(self.contrast_label)
        self.controls_layout.addLayout(slider_layout) 
        self.controls_layout.addSpacerItem(spacer_bottom)
        self.controls_layout.addWidget(self.apply_button)
        self.controls_layout.addWidget(self.download_button)

        # Widget pour afficher l'image
        self.image_widget = ImageWidget()

        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.image_widget)

    def open_file_dialog(self):
        """Ouvre un dialogue pour sélectionner 3 fichiers FIT."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez 3 fichiers FIT", "", "Fichiers FIT (*.fit)"
        )
        return files, _

    def set_image(self, rgb_image: np.ndarray):
        """Affiche l'image dans l'ImageWidget."""
        self.image_widget.setPixmap(rgb_image)
