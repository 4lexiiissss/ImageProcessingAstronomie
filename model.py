import numpy as np


class FITSModel:
    def __init__(self):
        self.rgb_image = None  # Stocke l'image RGB normalisée

    def set_rgb_image(self, image: np.ndarray):
        """Définit l'image RGB."""
        self.rgb_image = image

    def get_rgb_image(self) -> np.ndarray:
        """Retourne l'image RGB."""
        return self.rgb_image