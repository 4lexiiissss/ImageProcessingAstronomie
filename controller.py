from astropy.io import fits
from astropy.visualization import MinMaxInterval, ImageNormalize
import numpy as np
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

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
        data = fits.getdata(self.fit_files[0])  # Données pour H-alpha
        data2 = fits.getdata(self.fit_files[1])  # Données pour OIII
        data3 = fits.getdata(self.fit_files[2])  # Données pour SII

        # Fixer les plages de valeurs pour augmenter le contraste
        vmin, vmax = 10, 1000

        norm = ImageNormalize(data, vmin=vmin, vmax=vmax, interval=MinMaxInterval())
        norm2 = ImageNormalize(data2, vmin=vmin, vmax=vmax, interval=MinMaxInterval())
        norm3 = ImageNormalize(data3, vmin=vmin, vmax=vmax, interval=MinMaxInterval())

        # Créer l'image RGB en combinant les trois canaux
        rgb_image = np.dstack((norm3(data3), norm(data), norm2(data2)))

        # Afficher l'image dans la vue
        self.display_image(rgb_image)

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

    def display_image(self, rgb_image):
        """Affiche l'image RGB finale dans la vue."""
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            (rgb_image * 255).astype(np.uint8), width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.view.image_label.setPixmap(pixmap)
        self.view.image_label.setScaledContents(True)
