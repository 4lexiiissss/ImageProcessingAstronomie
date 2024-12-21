#   Copyright (C) 2024  Alexis Demol - Lucas Debruyne  
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# ImageProcessingAstronomie project 2024
# author: 
# Alexis Demol (4lexiiissss) | alexisdemol.europe@gmail.com 
# Lucas Debruyne (lucas210905) | lucas.debruyne2109@gmail.com

# import 
# -----------------------------------------------------------------------------
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSlider, QLabel, QSizePolicy, QSpacerItem, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
import numpy as np
from ImageWidget import ImageWidget

# ------------------------------------------------------------------------------------------
# --- class FITSView-------------------------------------------------------
# ------------------------------------------------------------------------------------------
class FITSView(QWidget):
    
    # methods
    # -------------------------------------------------- 
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("MY SPACE")
        self.main_layout = QHBoxLayout(self)

        self.controls_layout = QVBoxLayout()

        self.load_button = QPushButton("Charger 3 fichiers FIT")
        self.load_button.clicked.connect(self.controller.load_fit_files)
        self.load_button.setMaximumWidth(160)
        self.load_button.setMaximumHeight(30)

        self.contrast_label = QLabel("Contraste")
        self.contrast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        spacer_top = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        slider_layout = QVBoxLayout()

        # -------------------------------------------------- 
        def create_slider(label_text):
            layout = QVBoxLayout()
            slider_label = QLabel(label_text)
            slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_top = QLabel("100")
            label_bottom = QLabel("0")
            slider = QSlider(Qt.Orientation.Vertical)

            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setMinimumHeight(160)
            slider.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            slider.setMaximumWidth(20)

            layout.addWidget(slider_label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_top, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_bottom, alignment=Qt.AlignmentFlag.AlignCenter)

            return layout, slider

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
        self.download_button.clicked.connect(self.controller.download_images) 

        self.controls_layout.addWidget(self.load_button)
        self.controls_layout.addSpacerItem(spacer_top)
        self.controls_layout.addWidget(self.contrast_label)
        self.controls_layout.addLayout(slider_layout) 
        self.controls_layout.addSpacerItem(spacer_bottom)
        self.controls_layout.addWidget(self.apply_button)
        self.controls_layout.addWidget(self.download_button)

        self.image_widget = ImageWidget()

        self.main_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.image_widget)

    # -------------------------------------------------- 
    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez 3 fichiers FIT", "", "Fichiers FIT (*.fit)"
        )
        return files, _

    # -------------------------------------------------- 
    def set_image(self, rgb_image: np.ndarray):
        self.image_widget.setPixmap(rgb_image)

    # -------------------------------------------------- 
    def get_position(self):
        position, ok = QInputDialog.getText(self, "Position cible", "Entrez la position cible (par exemple, 'M51' ou '10.684,41.269') : ")
        if ok:
            return position
        else:
            return None
    
    # -------------------------------------------------- 
    def get_mission(self):
        mission, ok = QInputDialog.getText(self, "Nom de la mission", "Entrez le nom de la mission ou du survey (par exemple, 'DSS2') : ")
        if ok:
            return mission
        else:
            return None
    
    # -------------------------------------------------- 
    def get_output_directory(self):
        dossier_sortie = QFileDialog.getExistingDirectory(self, "Sélectionnez le dossier de sortie")
        return dossier_sortie

    # -------------------------------------------------- 
    def show_message(self, message):
        QMessageBox.information(self, "Information", message)

    # -------------------------------------------------- 
    def show_error_message(self, message):
        QMessageBox.critical(self, "Erreur", message)

    # -------------------------------------------------- 
    def get_red_slider_value(self):
        return self.red_slider.value()

    # -------------------------------------------------- 
    def get_green_slider_value(self):
        return self.green_slider.value()

    # -------------------------------------------------- 
    def get_blue_slider_value(self):
        return self.blue_slider.value()
