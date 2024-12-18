import os
import numpy as np
from astropy.io import fits
from model import FITSModel


class FITSController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.fit_files = []  # Stocke les chemins des fichiers FIT

    def load_fit_files(self):
        """Ouvre un dialogue pour charger 3 fichiers FIT."""
        file_paths, _ = self.view.open_file_dialog()
        if len(file_paths) != 3:
            print("Veuillez sélectionner exactement 3 fichiers FIT.")
            return
        
        self.fit_files = file_paths

        # Lire les fichiers FIT et créer une image RGB
        images = []
        for path in self.fit_files:
            try:
                with fits.open(path) as hdul:
                    image_data = hdul[0].data
                    images.append(image_data)
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {path}: {e}")
                return

        # Normaliser et combiner en RGB
        images = [self.normalize_image(img) for img in images]
        rgb_image = np.dstack(images)  # Combine les 3 canaux pour une image RGB

        # Sauvegarder l'image RGB en tant que fichier FITS
        output_path = self.save_as_fits(rgb_image)
        print(f"Fichier FITS créé : {output_path}")

        # Mettre à jour le modèle et activer l'affichage
        self.model.set_rgb_image(rgb_image)
        self.view.show_button.setEnabled(True)

    def save_as_fits(self, rgb_image):
        """Sauvegarde l'image RGB en tant que fichier FITS."""
        output_path = "output_combined.fits"
        hdu = fits.PrimaryHDU(rgb_image)
        hdu.writeto(output_path, overwrite=True)
        return output_path

    def display_image(self):
        """Affiche l'image RGB finale."""
        rgb_image = self.model.get_rgb_image()
        if rgb_image is not None:
            self.view.set_image(rgb_image)

    @staticmethod
    def normalize_image(image):
        """Normalise les valeurs d'une image FIT entre 0 et 1."""
        image = np.nan_to_num(image, nan=0.0)  # Remplacer NaN par 0
        min_val = np.min(image)
        max_val = np.max(image)
        return (image - min_val) / (max_val - min_val) if max_val > min_val else image