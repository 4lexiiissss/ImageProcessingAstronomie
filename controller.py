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
from astropy.io import fits
from astropy.visualization import MinMaxInterval, ImageNormalize, PercentileInterval
import numpy as np
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from astroquery.skyview import SkyView
import os

# ------------------------------------------------------------------------------------------
# --- class FITSController-------------------------------------------------------
# ------------------------------------------------------------------------------------------
class FITSController:
    
    # methods
    # -------------------------------------------------- 
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.fit_files = []  

    # -------------------------------------------------- 
    def load_fit_files(self):
        file_paths, _ = self.view.open_file_dialog()

        if len(file_paths) != 3:
            self.view.show_error_message("Veuillez sélectionner exactement 3 fichiers FIT.")
            return

        try:
            self.fit_files = []
            interval = PercentileInterval(99.5)
            for file_path in file_paths:
                data = fits.getdata(file_path)
                normalized_data = interval(data)
                normalized_data = np.nan_to_num(normalized_data, nan=0.0)
                self.fit_files.append(normalized_data)

            self.apply_changes()

        except Exception as e:
            self.view.show_error_message(f"Erreur lors du chargement des fichiers FIT: {str(e)}")


    # -------------------------------------------------- 
    def apply_changes(self):
        try:
            red_scale = self.view.get_red_slider_value() / 100
            green_scale = self.view.get_green_slider_value() / 100
            blue_scale = self.view.get_blue_slider_value() / 100

            adjusted_fit_files = [
                self.fit_files[0] * red_scale,
                self.fit_files[1] * green_scale,
                self.fit_files[2] * blue_scale
            ]

            norms = [
                ImageNormalize(data, interval=MinMaxInterval()) for data in adjusted_fit_files
            ]
            scaled_images = [norm(data) for norm, data in zip(norms, adjusted_fit_files)]

            rgb_image = np.dstack(scaled_images)
            rgb_image = np.clip(rgb_image, 0, 1)  

            self.model.set_rgb_image(rgb_image)
            self.view.set_image(rgb_image)

        except Exception as e:
            self.view.show_error_message(f"Erreur lors de l'application des changements: {str(e)}")

    # -------------------------------------------------- 
    def display_image(self, rgb_image):
        height, width, _ = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            (rgb_image * 255).astype(np.uint8), width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.view.image_widget.setPixmap(pixmap)
        self.view.image_widget.setScaledContents(True)

    # -------------------------------------------------- 
    def download_images(self):
        position = self.view.get_position()
        mission = self.view.get_mission()
        dossier_sortie = self.view.get_output_directory()
        if not position or not mission or not dossier_sortie:
            self.view.show_error_message("Tous les champs doivent être renseignés.")
            return

        try:
            telecharger_donnees_rgb(position, mission, dossier_sortie)
            self.view.show_message("Téléchargement terminé avec succès.")
        except Exception as e:
            self.view.show_error_message(f"Erreur lors du téléchargement des images : {str(e)}")

# -------------------------------------------------- 
def telecharger_donnees_rgb(position, mission, dossier_sortie):
    surveys_rgb = {
        "rouge": f"{mission} Red",
        "vert": f"{mission} IR",
        "bleu": f"{mission} Blue"
    }
    os.makedirs(dossier_sortie, exist_ok=True)

    for couleur, survey in surveys_rgb.items():
        try:
            print(f"Téléchargement de la bande {couleur} ({survey})...")
            fits_files = SkyView.get_images(position=position, survey=[survey])
            for i, fits_file in enumerate(fits_files):
                file_path = os.path.join(dossier_sortie, f"{couleur}_image_{i + 1}.fit")
                fits_file[0].writeto(file_path, overwrite=True)
                print(f"Fichier téléchargé : {file_path}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de la bande {couleur} ({survey}) : {e}")
