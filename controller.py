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

        try:
            self.fit_files = [fits.getdata(file_path) for file_path in file_paths]

            self.fit_files = [np.clip(data, 10, 1000) for data in self.fit_files]

            # Appliquer les changements pour la première fois
            self.apply_changes()

        except Exception as e:
            self.view.show_error_message(f"Erreur lors du chargement des fichiers FIT: {str(e)}")

    def apply_changes(self):
        """Applique les changements de contraste et met à jour l'image."""
        try:
            # Récupérer les valeurs des curseurs
            red_scale = self.view.red_slider.value() / 100.0
            green_scale = self.view.green_slider.value() / 100.0
            blue_scale = self.view.blue_slider.value() / 100.0

            # Ajuster les niveaux de chaque image
            adjusted_fit_files = [
                self.fit_files[0] * red_scale,
                self.fit_files[1] * green_scale,
                self.fit_files[2] * blue_scale
            ]

            vmin, vmax = 10, 1000
            norms = [ImageNormalize(data, vmin=vmin, vmax=vmax, interval=MinMaxInterval()) for data in adjusted_fit_files]

            rgb_image = np.dstack([norm(data) for norm, data in zip(norms, adjusted_fit_files)])

            self.model.set_rgb_image(rgb_image)
            self.view.set_image(rgb_image)

        except Exception as e:
            self.view.show_error_message(f"Erreur lors de l'application des changements: {str(e)}")

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


# # Class object for downloading images from MAST ending by .fits
# class SpaceDownload:
#     def __init__(self, images_folder="images"):
#         self.images_folder = images_folder

#     def search_observations(self, object_name):
#         print(f"Searching observations for {object_name}...")
#         # find observations for the given object name within a small radius
#         results = Observations.query_object(object_name, radius="0.1 deg")
#         print(f"Found {len(results)} results.")
#         return results

#     def download_observation(self, obs_id):
#         print(f"Downloading observation {obs_id}...")
#         # Get the list of data products available for the observation
#         data_products = Observations.get_product_list(obs_id)
        
#         # only fits files / take the list of data and add an filter 
#         fitImage = Observations.filter_products(data_products, extension="fits")
        
#         # if fits file is found, download them else no 
#         if len(fitImage) > 0:
#             manifest = Observations.download_products(fitImage, download_dir=self.images_folder)
#             print("Download complete.")
#             return manifest
#         else:
#             print("No FITS files found for this observation.")
#             return None

# if __name__ == "__main__":
#     space_obs = SpaceDownload()

#     while True:
#         # until the user said stop 
#         object_name = input("Enter the name of the celestial object to search (or 'STOP' to cancel): ")
#         if object_name.upper() == "STOP":
#             print("Program stopped.")
#             break
        
#         results = space_obs.search_observations(object_name)
#         if len(results) > 0:
#             # show all the list observations with their id 
#             for i, result in enumerate(results):
#                 print(f"[{i}] Obs ID: {result['obsid']}, Target: {result['target_name']}")

#             # the user can select the ID of the observation that can be download
#             choice = input("Enter the index of the observation to download: ([0][1]etc..)")
#             # validation user input
#             if choice.isdigit() and int(choice) < len(results):  
#                 obs_id = results[int(choice)]['obsid']  
#                 space_obs.download_observation(obs_id)  
#             else:
#                 print("Invalid choice. Please enter a valid index.")
#         else:
#             print(f"No observations found for {object_name}.")