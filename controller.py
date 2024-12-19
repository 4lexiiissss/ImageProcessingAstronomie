from astropy.io import fits
from astropy.visualization import MinMaxInterval, ImageNormalize
import numpy as np
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class FITSController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.fit_files = []  

    def load_fit_files(self):
        """Ouvre un dialogue pour charger 3 fichiers FIT."""
        file_paths, _ = self.view.open_file_dialog()

        if len(file_paths) != 3:
            self.view.show_error_message("Veuillez sélectionner exactement 3 fichiers FIT.")
            return

        self.fit_files = file_paths

        data = fits.getdata(self.fit_files[0])  
        data2 = fits.getdata(self.fit_files[1])  
        data3 = fits.getdata(self.fit_files[2])  
        
        # Remplacer les valeurs extrêmes par 0
        data = np.where((data > 1000) | (data < 10), 0, data)
        data2 = np.where((data2 > 1000) | (data2 < 10), 0, data2)
        data3 = np.where((data3 > 1000) | (data3 < 10), 0, data3)

        vmin, vmax = 10, 1000
        norm = ImageNormalize(data, vmin=vmin, vmax=vmax, interval=MinMaxInterval())
        norm2 = ImageNormalize(data2, vmin=vmin, vmax=vmax, interval=MinMaxInterval())
        norm3 = ImageNormalize(data3, vmin=vmin, vmax=vmax, interval=MinMaxInterval())

        rgb_image = np.dstack((norm(data3), norm3(data), norm2(data2)))

        self.model.set_rgb_image(rgb_image)
        self.view.set_image(rgb_image)

    def save_as_fits(self, rgb_image):
        output_path = "output_combined.fits"
        hdu = fits.PrimaryHDU(rgb_image)
        hdu.writeto(output_path, overwrite=True)
        return output_path

    def display_image(self, rgb_image):
        height, width = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            (rgb_image * 255).astype(np.uint8), width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.view.image_label.setPixmap(pixmap)
        self.view.image_label.setScaledContents(True)
